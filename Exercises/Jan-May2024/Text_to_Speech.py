from newspaper import Article
from gtts import gTTS
import nltk
nltk.download('punkt')

url = input("Please input the url of a news article you wish to have converted to speech: ")

news_article = Article(url)
news_article.download()
news_article.parse()

content_to_convert = f"Title: {news_article.title}\n"
content_to_convert += f"Authors: {news_article.authors}\n"
content_to_convert += f"Publish Date: {news_article.publish_date}\n"
content_to_convert += f"Main Article: {news_article.text}"

tts = gTTS(content_to_convert, lang='en')
tts.save('C:\\Users\\Andre\\Downloads\\Converted_Article.mp3')