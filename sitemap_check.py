import requests
import streamlit as st
import advertools as adv
import pandas as pd

urls_dict = {
	'URL': [],
	'Status Code': [],
	'Status': []
}

st.header('Is it really not in the sitemap?')

st.info("This script takes a CSV export of 'Primary Pages Not in Sitemaps' from Lumar and checks the site's sitemap to see if they really are missing.")

# urls_to_check = st.text_area('Enter the URLs you want to check, one per line')

crawl_csv = st.file_uploader('Upload your Lumar CSV file')
urls_to_check = st.text_area('Or add a list of URLs to check, 1 per line')
sitemap_link = st.text_input('Enter XML sitemap to check')
submit = st.button('Submit')

if submit and crawl_csv:

	crawl_csv_url_list = pd.read_csv(crawl_csv)['url'].tolist()
	sitemap_df = adv.sitemap_to_df(sitemap_link)
	sitemap_url_list = sitemap_df['loc'].to_list()

	for url in crawl_csv_url_list:
		urls_dict['URL'].append(url)
		status_code = requests.get(url).status_code
		urls_dict['Status Code'].append(status_code)
		if url in sitemap_url_list:			
			urls_dict['Status'].append('Found in sitemap')
		else:
			urls_dict['Status'].append('Not found in sitemap')

elif submit and urls_to_check:

	sitemap_df = adv.sitemap_to_df(sitemap_link)
	sitemap_url_list = sitemap_df['loc'].to_list()

	url_list = [url for url in urls_to_check.split('\n')]

	for u in url_list:
		urls_dict['URL'].append(u)
		status_code = requests.get(u).status_code
		urls_dict['Status Code'].append(status_code)
		if u in sitemap_url_list:			
			urls_dict['Status'].append('Found in sitemap')
		else:
			urls_dict['Status'].append('Not found in sitemap')


	df = pd.DataFrame(urls_dict)
	st.dataframe(df)
	df_csv = df.to_csv(index=False)
	st.download_button(label="Download data as CSV", data=df_csv, file_name=f"{sitemap_link}_urls_in_sitemap.csv", mime='text/csv')