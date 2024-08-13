import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

user_input = input("Please enter symbol you are looking for news on: ")

url_templates = {
    'Yahoo': f'https://finance.yahoo.com/quote/{user_input.upper()}',
    'CNBC': f'https://cnbc.com/quotes/{user_input}?qsearchterm={user_input}',
    'Motley Fool': f'https://fool.com/quote/nyse/{user_input}',
    #'Morningstar': f'https://www.morningstar.ca/ca/funds/SecuritySearchResults.aspx?search={user_input}&type=',
    #'Forbes': f'https://forbes.com/search?q={user_input}',
    #'Benzinga': f'https://benzinga.com/quote/{user_input}',
    #'Financial Times': f'https://ft.com/search?q={user_input}'
}

#lookup and get company search terms
lookup_response = requests.get(url_templates['Yahoo'])
lookup_soup = BeautifulSoup(lookup_response.text, 'html.parser')
html_string = str(lookup_soup.find('h1', string=lambda text: user_input.upper() in text.strip()))
exchange_lookup = str(lookup_soup.find('span', class_=re.compile(r'.*exchange.*')))
exchange_regex_search = re.search(r'<span>(.*?)</span>', exchange_lookup)
exchange = exchange_regex_search.group(1)
exchange = exchange.split()
exchange = exchange[0]
print(exchange)
name_regex_search = re.search(r'<h1[^>]*>(.*?)</h1>', html_string)
company_data = name_regex_search.group(1)
company_data = company_data.split(',')
print(company_data)

#cleaning and formatting data

news_data = {}

for site, url in url_templates.items():
    response = requests.get(url)
    print(site)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if site == 'Yahoo':
            for item in soup.find_all('a', class_=lambda value: value and 'subtle-link' and 'title' in value):
                headline = item.text
                link = item.get('href')
                news_data[headline] = link
        elif site == 'CNBC':
            for item in soup.find_all('a', class_=lambda value: value and 'LatestNews' in value):
                headline = item.text
                link = item.get('href')
                news_data[headline] = link
        elif site == 'Motley Fool':
            for item in soup.find_all('a', attrs={'data-track-category': 'quotepage_news_analysis'}):
                headline = item.text
                if item.get('href'):
                    link = f'fool.com{item.get('href')}'
                    news_data[headline] = link

            """
            for item in soup.find_all('a', attributes={'data-track-category': 'quotepage_news_analysis'}):
                print(item)
        
        index = 0
        for :
            if user_input.lower() in item.text.strip().lower() or company_data[0].lower() in item.text.strip().lower():
                headline = item.text.strip()
                link = item['href']
                news_data[index] = {'Headline': headline, 'Link': link}
                index += 1
            """

news_df = pd.DataFrame.from_dict(news_data, orient='index')

#news_df.to_excel('news_df.xlsx', sheet_name='News Headlines', index=False)
