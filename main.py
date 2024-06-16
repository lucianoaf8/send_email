from dotenv import load_dotenv
import requests
import os
from datetime import datetime
from send_email import send_email

# Load environment variables from .env file
load_dotenv()

# Path to the file storing the counter
COUNTER_FILE = 'counter.txt'
TEST_SEND_TO = os.getenv("NEWS_API_KEY")

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
        top_news.append(f"<a href='{article['url']}'>{article['title']}</a>")

    return top_news

def get_crossword():
    # Placeholder for the crossword content
    return "1. Across: First letter of the alphabet (1)\n2. Down: First vowel (1)"

def update_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'w') as f:
            f.write('0')
    
    with open(COUNTER_FILE, 'r+') as f:
        counter = int(f.read().strip())
        counter += 1
        f.seek(0)
        f.write(str(counter))
        f.truncate()
    
    return counter

def create_email_content():
    # Update the counter
    counter = update_counter()

    # Get the quote
    # quote = get_quote()

    # Get the top news
    # api_key = os.getenv("NEWS_API_KEY")
    # ai_news = get_top_news(api_key, "AI", 3)
    # data_science_news = get_top_news(api_key, "Data Science", 3)
    # tech_news = get_top_news(api_key, "Technology", 3)

    # # Get the crossword
    # crossword = get_crossword()

    # Create the email content
    email_body = f"""
    <h1>{counter} days going strong</h1>
    """

    return email_body

if __name__ == "__main__":
    # Email details
    subject = f"{update_counter()} days going strong"
    to_email = TEST_SEND_TO
    html_content = create_email_content()

    # Send the email
    send_email(subject, to_email, html_content)
