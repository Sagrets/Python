#Library and module imports
import datasets
import requests
import json
import re
from newsapi import NewsApiClient
import pandas as pd
from newspaper import Article
from bs4 import BeautifulSoup
from transformers import pipeline, AutoTokenizer

#Taking user input
symbol = input('Enter the stock symbol or search term you are looking for news on: ')
from_date = input('Please enter a starting date for which to scape news from, use yyyy-mm-dd format. This input is optional, leave it blank and hit enter to skip: ')
to_date = input('Please enter a end date for which to scape news from, use yyyy-mm-dd format. This input is optional, leave it blank and hit enter to skip: ')

#prepping urls and APIs
stock_news = requests.get(f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey=KLYIA9KV3ARAL5BB').json()
yahoo_url = f'https://finance.yahoo.com/quote/{symbol.upper()}'
newsapi = NewsApiClient(api_key='8f3dc4803c8d4a87bf7a7da5504554a7')

#Company name lookup
name_string = (
        re.search(r'<h1[^>]*>(.*?)</h1>', str(BeautifulSoup(requests.get(yahoo_url).text, 
        'html.parser').find('h1', string=lambda text: symbol.upper() in text.strip()))).group(1)
    )

if '?' in name_string:
    company_name = name_string.split('?')[0]
elif ',' in name_string:
    company_name = name_string.split(',')[0]
elif '.' in name_string:
    company_name = name_string.split('.')[0]

#Exchange lookup
exchange = (
    re.search(r'<span>(.*?)</span>', str(BeautifulSoup(requests.get(yahoo_url).text, 
    'html.parser').find('span', class_=re.compile(r'.*exchange')))).group(1).split()[0]
    )

#Headline scrapping
if from_date and to_date:
    newsapi.get_everything(q=symbol, from_param=from_date, to=to_date)
else:
    news_articles_v1 = newsapi.get_everything(q=symbol)

news_dict = {}

for item in news_articles_v1['articles']:
    if company_name in item['title'] or symbol in item['title']:
        news_dict[item['title']] = item['url']

if 'feed' in stock_news:
    for item in stock_news['feed']:
        if company_name in item['title'] or symbol in item['title']:
            news_dict[item['title']] = item['url']
else:
    print('Alphavantage daily API limit hit.')


#Function to download and parse article
def article_parse(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
    
        return article.text
    
    except Exception as failed_download:
        return None

#Scrapping and compiling the articles
scrapped_content = ''

for headline, url in news_dict.items():
    tmp = article_parse(url)

    if tmp != None:
        scrapped_content += 2 * '\n'
        scrapped_content += 8 * '-'
        scrapped_content += 2 * '\n'
        scrapped_content += tmp

#Article text preprocessing
scrapped_content = scrapped_content.lower()
scrapped_content = re.sub(r'[^\w\s]', '', scrapped_content)

#Chunking articles
chunked_articles = []
for i in range(0, len(scrapped_content) - 1, 255):
    chunked_articles.append(scrapped_content[i:i+255])


pipe = pipeline(
    'text-classification', 
    model='mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis',
    max_length=255,
    padding=True
                )
sentiment_results = []


for chunk in chunked_articles:
    sentiment_results.append(pipe(chunk))

def calc_weighted_confidence_scores(sentiment):
    total_score = 0
    total_weight = 0
    for result, chunk in zip(sentiment_results, chunked_articles):
        if result[0]['label'] == sentiment:
            sentiment_score = result[0]['score']
            chunk_weight = len(chunk)
            total_score += sentiment_score * chunk_weight
            total_weight += chunk_weight
    average_sentiment = total_score / total_weight

    return average_sentiment

final_sentiment_scores = [
    {'Name':'positive', 'Count': 0, 'Score': calc_weighted_confidence_scores('positive')}, 
    {'Name': 'negative', 'Count': 0, 'Score': calc_weighted_confidence_scores('negative')},
    {'Name': 'neutral', 'Count': 0, 'Score': calc_weighted_confidence_scores('neutral')}
                          ]

for item in sentiment_results:
    if item[0]['label'] == 'positive':
        final_sentiment_scores[0]['Count'] += 1
    if item[0]['label'] == 'negative':
        final_sentiment_scores[1]['Count'] += 1
    if item[0]['label'] == 'neutral':
        final_sentiment_scores[2]['Count'] += 1

print(final_sentiment_scores)
