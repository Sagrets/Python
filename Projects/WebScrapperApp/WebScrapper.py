import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

symbol = input('Enter the stock symbol you are looking for news on: ')

url_list = {
            'Yahoo': f'https://finance.yahoo.com/quote/{symbol.upper()}',
            #'CNBC': f'https://cnbc.com/quotes/{stock}?qsearchterm={stock}',
            #'Motley Fool': f'https://fool.com/quote/nyse/{stock}',
            #'Morningstar': f'https://www.morningstar.ca/ca/funds/SecuritySearchResults.aspx?search={stock}&type=',
            #'Forbes': f'https://forbes.com/search?q={stock}',
            #'Benzinga': f'https://benzinga.com/quote/{stock}',
            #'Financial Times': f'https://ft.com/search?q={stock}'  
        }


class site_properties:
    def __init__(self, stock, site):
        self.url = url_list[site]

        #Company name search and cleaning
        self.name_string = (
            re.search(r'<h1[^>]*>(.*?)</h1>', str(BeautifulSoup(requests.get(url_list['Yahoo']).text, 
                'html.parser').find('h1', string=lambda text: stock.upper() in text.strip()))).group(1)
        )

        if ',' in self.name_string:
            self.company_name = self.name_string.split(',')[0]
        elif '.' in self.name_string:
            self.company_name = self.name_string.split('.')[0]

        #Exchange lookup
        self.exchange = (
            re.search(r'<span>(.*?)</span>', str(BeautifulSoup(requests.get(url_list['Yahoo']).text, 
                'html.parser').find('span', class_=re.compile(r'.*exchange')))).group(1).split()[0]
        )

        #Empty dataframe to hold news headlines and URLs
        self.news_dict = {}

    def get_headlines(self):
        for site, url in url_list.items():
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                if site == 'Yahoo':
                    for item in soup.find_all('a', class_=lambda value: value and 'subtle-link' and 'title'):
                        if self.company_name in item.text or symbol in item.text:
                            self.news_dict[item.text] = item.get('href')
        
        self.news_df = pd.DataFrame.from_dict(self.news_dict, orient='index')
        
#The building of a dictonary containing site properties objects
site_objects = {}

for site, url in url_list.items():
    temp = site_properties(symbol, site)
    site_objects[site] = temp

site_objects['Yahoo'].get_headlines()

print(site_objects['Yahoo'].news_dict)