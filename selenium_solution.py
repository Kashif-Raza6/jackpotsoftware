import time, json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
import pandas as pd
from bs4 import BeautifulSoup
import re


def scroll_page(url):
    service = Service(executable_path="chromedriver")

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--lang=en")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    )
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    old_height = driver.execute_script("""
    	function getHeight() {
    		return document.querySelector('.zxU94d').scrollHeight;
    	}
    	return getHeight();
    """)

    while True:
        driver.execute_script(
            "document.querySelector('.zxU94d').scrollTo(0, document.querySelector('.zxU94d').scrollHeight)"
        )

        time.sleep(2)

        new_height = driver.execute_script("""
    		function getHeight() {
    			return document.querySelector('.zxU94d').scrollHeight;
    		}
    		return getHeight();
    	""")

        if new_height == old_height:
            break

        old_height = new_height

    selector = Selector(driver.page_source)

    driver.quit()

    return selector


def scrape_google_jobs(selector):
    google_jobs_results = []

    for result in selector.css('.iFjolb'):
        title = result.css('.BjJfJf::text').get()
        company = result.css('.vNEEBe::text').get()

        container = result.css('.Qk80Jf::text').getall()
        location = container[0]
        via = container[1]

        thumbnail = result.css('.pJ3Uqf img::attr(src)').get()
        extensions = result.css('.KKh3md span::text').getall()
        description = result.css('.WbZuDe::text').get()
        url = result.css('.pMhGee.Co68jc.j0vryd.zixIx::attr(href)').get()
      


        google_jobs_results.append({
            'title': title,
            'company': company,
            'location': location,
            'via': via,
            'thumbnail': thumbnail,
            'extensions': extensions,
            'description': description,
            'url': url
            
        })

    print(json.dumps(google_jobs_results, indent=2, ensure_ascii=False))
    print(len(google_jobs_results))
    df = pd.DataFrame(google_jobs_results,
                      columns=[
                          'title', 'company', 'location',  'via',
                          'extensions', 'description', 'url'
                      ])
    # store the results in a csv file
    df.to_csv('google_jobs_results.csv', index=True)
    return df


def selenium_scrape(job_title):
    params = {
        'q': job_title,                             # job title as the search string
        'ibp': 'htl;jobs',                          # google jobs
        'uule': 'w+CAIQICINVW5pdGVkIFN0YXRlcw',     # encoded location (USA)
        'hl': 'en',                                 # language
        'gl': 'us',                                 # country of the search
    }
    
    URL = f"https://www.google.com/search?q={params['q']}&ibp={params['ibp']}&uule={params['uule']}&hl={params['hl']}&gl={params['gl']}"
    
    result = scroll_page(URL)
    data = scrape_google_jobs(result)
    return data
