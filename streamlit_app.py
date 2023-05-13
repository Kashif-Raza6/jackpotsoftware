from langchain.llms.openai import OpenAI
from langchain.document_loaders import TextLoader
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
load_dotenv()

st.markdown("""
<style>
body {
    color: #fff;
    background-color: #4F8BF9;
}
</style>
    """, unsafe_allow_html=True)

# st.image('logo.png', use_column_width=True)

st.title("Job Search Chatbot 🔍🧠💼🤖")
st.sidebar.header("Upload txt File")

# st.header("Job Search Chatbot")
st.write("This is a chatbot that will help you find a job.")
st.write("Please upload your CV on the sidebar to get started.")

uploaded_file = st.sidebar.file_uploader("Choose a CV", type="txt")
job_location = st.sidebar.selectbox('Select job location:', ['USA', 'Canada', 'UK', 'Australia'])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    st.sidebar.success("File uploaded successfully!")

    def embedding(file_name):
        loader = TextLoader(file_name, encoding='utf8')
        from langchain.indexes import VectorstoreIndexCreator
        index = VectorstoreIndexCreator().from_loaders([loader])
        return index

    with st.spinner('Embedding the file...'):
        index = embedding(temp_file_path)

    query = "What is the Study Background and experience of the candidate?"
    result= index.query(query)

    chat_model = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

    instructions = """
    You will be given a sentence which include the study background and experience of the candidate, Extract the
    study background and experience of the candidate in 4 words: {result}  
    """
    study_background = """
    Computer Science, Web Development
    """
    prompt = (instructions + study_background)
    
    with st.spinner('Extracting the information...'):
        output = chat_model([HumanMessage(content=prompt)])

    from langchain.utilities import GoogleSerperAPIWrapper
    search = GoogleSerperAPIWrapper()

    try:
        with st.spinner('Searching for jobs...'):
            search_result = search.run(f"{output.content} Jobs in {job_location}")
        st.success('Search completed!')
    except Exception as e:
        st.error(f'Error: {e}')

    st.write('------------------------')
    st.header('Search Result')
    st.write(search_result)
