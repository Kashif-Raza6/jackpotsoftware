from serpapi import GoogleSearch
import os, json

params = {
	# https://docs.python.org/3/library/os.html#os.getenv
	'api_key': os.getenv('429c9aa457078fd435e39adb7096372cf432b62d8e6c908709857b89a45c012c'),    		# your serpapi api
	# https://site-analyzer.pro/services-seo/uule/
	'uule': 'w+CAIQICINVW5pdGVkIFN0YXRlcw',		# encoded location (USA)
	'q': 'python backend',              		# search query
    'hl': 'en',                         		# language of the search
    'gl': 'us',                         		# country of the search
	'engine': 'google_jobs',					# SerpApi search engine
	'start': 0                                  # pagination
}


def serpapi_scrape():
	google_jobs_results = []
	
	while True:
	    search = GoogleSearch(params)               # where data extraction happens on the SerpApi backend
	    result_dict = search.get_dict()             # JSON -> Python dict
	
	    if 'error' in result_dict:
	        break
	    
	    for result in result_dict['jobs_results']:
	        google_jobs_results.append(result)
	
	    params['start'] += 10
	
	print(json.dumps(google_jobs_results, indent=2, ensure_ascii=False))