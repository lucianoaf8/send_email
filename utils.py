from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    quote_data = response.json()[0]
    quote = f"{quote_data['q']} - {quote_data['a']}"
    return quote
  
def get_top_news(api_key, query, num_articles=5):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&pageSize={num_articles}&sortBy=publishedAt"
    response = requests.get(url)
    news_data = response.json()

    top_news = []
    for article in news_data['articles']:
        top_news.append({"title": article['title'], "url": article['url']})

    return top_news

