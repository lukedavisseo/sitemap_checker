import requests
import streamlit as st
import advertools as adv
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

urls_dict = {
	'URL': [],
	'Status Code': [],
	'Status': []
}

st.header('Is it really not in the sitemap?')

st.info("This script takes a CSV export of 'Primary Pages Not in Sitemaps' from Lumar and checks the site's sitemap to see if they really are missing.")

crawl_csv = st.file_uploader('Upload a CSV file that includes a list of URLs')
urls_to_check = st.text_area('Or add a list of URLs to check, 1 per line')
sitemap_link = st.text_input('Enter XML sitemap to check')
include_status_code = st.checkbox('Turn off status code checker', value=True)
submit = st.button('Submit')

if submit and crawl_csv:

	read_crawl_csv = pd.read_csv(crawl_csv)
	crawl_csv = read_crawl_csv.filter(regex='^[uU](rl$|RL$|rls$|RLs$)')
	crawl_csv_url_list = crawl_csv.iloc[:,0].to_list()
	sitemap_df = adv.sitemap_to_df(sitemap_link)
	sitemap_url_list = sitemap_df['loc'].to_list()

	for u in crawl_csv_url_list:
		urls_dict['URL'].append(u)
		if not include_status_code:
			status_code = requests.get(u, headers=headers).status_code
			urls_dict['Status Code'].append(status_code)
			if u in sitemap_url_list:			
				urls_dict['Status'].append('Found in sitemap')
			else:
				urls_dict['Status'].append('Not found in sitemap')
		else:
			if u in sitemap_url_list:			
				urls_dict['Status'].append('Found in sitemap')
			else:
				urls_dict['Status'].append('Not found in sitemap')
			urls_dict['Status Code'].append("-")

elif submit and urls_to_check:

	sitemap_df = adv.sitemap_to_df(sitemap_link)
	sitemap_url_list = sitemap_df['loc'].to_list()

	url_list = [url for url in urls_to_check.split('\n')]

	for u in url_list:
		urls_dict['URL'].append(u)
		if not include_status_code:
			status_code = requests.get(u, headers=headers).status_code
			urls_dict['Status Code'].append(status_code)
			if u in sitemap_url_list:			
				urls_dict['Status'].append('Found in sitemap')
			else:
				urls_dict['Status'].append('Not found in sitemap')
		else:
			if u in sitemap_url_list:			
				urls_dict['Status'].append('Found in sitemap')
			else:
				urls_dict['Status'].append('Not found in sitemap')
			urls_dict['Status Code'].append("-")


	df = pd.DataFrame(urls_dict)
	st.dataframe(df)
	df_csv = df.to_csv(index=False)
