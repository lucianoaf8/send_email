# main.py

import os
import sys
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
import pytz
from send_email import send_email
import http.client
import urllib.parse
import json
import random

print("Script started.")

print("Script started.")

# Load environment variables from .env file
load_dotenv()
print("Environment variables loaded.")

# Path to the file storing the counter
COUNTER_FILE = 'counter.txt'
TEST_SEND_TO = os.getenv("TEST_SEND_TO")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
USER_NAME = os.getenv("USER_NAME")
USER_CITY = os.getenv("USER_CITY")
USER_COUNTRY = os.getenv("USER_COUNTRY")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
THENEWSAPI_KEY = os.getenv("THENEWSAPI_KEY")

# Set up logging
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
    print(f"Created log folder: {log_folder}")

log_filename = os.path.join(log_folder, f"email_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("Logging initialized.")
print(f"Logging to: {log_filename}")

def get_gif():
    logging.info("Fetching GIF of the day.")
    response = requests.get(f"https://api.giphy.com/v1/gifs/random?tag=motivational&api_key={GIPHY_API_KEY}")
    gif_data = response.json()['data']
    gif_url = gif_data['images']['original']['url']
    logging.info(f"GIF URL: {gif_url}")
    return gif_url

def get_quote():
    logging.info("Fetching quote of the day.")
    response = requests.get("https://api.quotable.io/random?tags=inspirational")
    quote_data = response.json()
    quote = f"{quote_data['content']} - {quote_data['author']}"
    logging.info(f"Quote: {quote}")
    return quote

def get_weather():
    logging.info("Fetching weather forecast.")
    print("Fetching weather forecast.")
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={USER_CITY},{USER_COUNTRY}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        weather_data = response.json()
        
        if 'main' not in weather_data:
            logging.error(f"Unexpected API response: {weather_data}")
            print(f"Unexpected API response: {weather_data}")
            return "Weather data unavailable"
        
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        result = f"{temp:.1f}°C, {description}"
        logging.info(f"Weather fetched successfully: {result}")
        print(f"Weather fetched successfully: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather: {e}")
        print(f"Error fetching weather: {e}")
        return "Weather data unavailable"
    except KeyError as e:
        logging.error(f"Error parsing weather data: {e}")
        print(f"Error parsing weather data: {e}")
        return "Weather data unavailable"
    except Exception as e:
        logging.error(f"Unexpected error in get_weather: {e}")
        print(f"Unexpected error in get_weather: {e}")
        return "Weather data unavailable"

def get_this_day_in_history():
    logging.info("Fetching this day in history.")
    today = datetime.now()
    month, day = today.month, today.day
    response = requests.get(f"https://history.muffinlabs.com/date/{month}/{day}")
    data = response.json()
    event = data['data']['Events'][0]  # Get the first event
    return f"{event['year']}: {event['text']}"

def get_weather_icon(description):
    # Map weather descriptions to more detailed weather icons (using emoji for simplicity)
    weather_icons = {
        'clear sky': '☀️',
        'few clouds': '🌤️',
        'scattered clouds': '⛅',
        'broken clouds': '☁️',
        'shower rain': '🌦️',
        'rain': '🌧️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️'
    }
    return weather_icons.get(description.lower(), '🌡️')  # Default to thermometer if no match

def get_weather_tip(description):
    # Provide weather-specific tips
    tips = {
        'clear sky': "It's a beautiful day! Consider outdoor activities.",
        'few clouds': "Mild weather ahead. Perfect for a walk!",
        'scattered clouds': "Partly cloudy skies. Don't forget your sunglasses!",
        'broken clouds': "Cloudy with some sun. Dress in layers!",
        'shower rain': "Light rain expected. Grab an umbrella!",
        'rain': "Rainy day ahead. Stay dry and cozy!",
        'thunderstorm': "Storms brewing. Stay indoors and stay safe!",
        'snow': "Snow day! Bundle up and watch out for icy patches.",
        'mist': "Misty conditions. Drive carefully and use fog lights."
    }
    return tips.get(description.lower(), "Check the forecast for detailed weather information.")

def fetch_news(topic, num_articles=3):
    """Fetch news articles for a given topic."""
    url = f"https://news.google.com/rss/search?q={topic}&hl=en-CA&gl=CA&ceid=CA:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')[:num_articles]
    
    articles = []
    for item in items:
        article = {
            'title': item.title.text,
            'link': item.link.text,
            'pub_date': item.pubDate.text
        }
        articles.append(article)
    
    return articles

def generate_crosswords(num_puzzles=5):
    """Generate multiple crossword puzzles."""
    words = [
        "PYTHON", "ALGORITHM", "DATABASE", "FUNCTION", "VARIABLE",
        "LOOP", "ARRAY", "STRING", "INTEGER", "BOOLEAN",
        "CLASS", "OBJECT", "METHOD", "INHERITANCE", "POLYMORPHISM",
        "API", "FRAMEWORK", "LIBRARY", "DEBUGGING", "COMPILER"
    ]
    puzzles = []
    for _ in range(num_puzzles):
        word = random.choice(words)
        words.remove(word)  # Ensure no repetition
        puzzle = ["_" * len(word)]
        clue = f"A {len(word)}-letter word related to programming"
        puzzles.append((puzzle[0], word, clue))
    return puzzles

def get_historical_birthdays():
    """Fetch important people born on this day."""
    today = datetime.now()
    month, day = today.month, today.day
    url = f"https://history.muffinlabs.com/date/{month}/{day}"
    response = requests.get(url)
    data = response.json()
    births = data['data']['Births'][:3]  # Get top 3 births
    return [f"{person['year']}: {person['text']}" for person in births]

def get_historical_deaths():
    """Fetch important people who died on this day."""
    today = datetime.now()
    month, day = today.month, today.day
    url = f"https://history.muffinlabs.com/date/{month}/{day}"
    response = requests.get(url)
    data = response.json()
    deaths = data['data']['Deaths'][:3]  # Get top 3 deaths
    return [f"{person['year']}: {person['text']}" for person in deaths]

def get_fun_fact():
    logging.info("Fetching fun fact.")
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    fact_data = response.json()
    return fact_data['text']

def update_counter():
    logging.info("Updating counter.")
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'w') as f:
            f.write('0')
    
    with open(COUNTER_FILE, 'r+') as f:
        counter = int(f.read().strip())
        counter += 1
        f.seek(0)
        f.write(str(counter))
        f.truncate()
    
    logging.info(f"Counter updated to: {counter}")
    return counter

def get_weather_icon(description):
    # Map weather descriptions to Font Awesome icons
    weather_icons = {
        'clear sky': '☀️',
        'few clouds': '🌤️',
        'scattered clouds': '⛅',
        'broken clouds': '☁️',
        'shower rain': '🌦️',
        'rain': '🌧️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️'
    }
    return weather_icons.get(description.lower(), '🌡️')  # Default to thermometer if no match

def create_email_content(counter):
    print("Creating email content.")
    logging.info("Creating email content.")
    
    try:
        gif_url = get_gif()
        quote = get_quote()
        weather = get_weather()
        weather_description = weather.split(',')[1].strip()
        weather_icon = get_weather_icon(weather_description)
        weather_tip = get_weather_tip(weather_description)
        history_fact = get_this_day_in_history()
        fun_fact = get_fun_fact()
        
        # Fetch news for AI topics
        ai_news = fetch_news("Artificial Intelligence")
        ai_dev_news = fetch_news("AI Development")
        prompt_eng_news = fetch_news("Prompt Engineering")
        
        # Generate crosswords
        crosswords = generate_crosswords(5)
        
        # Get historical birthdays and deaths
        birthdays = get_historical_birthdays()
        deaths = get_historical_deaths()
        
    except Exception as e:
        print(f"Error while fetching content: {e}")
        logging.error(f"Error while fetching content: {e}")
        raise

    # Get the current date in the user's timezone
    current_date = datetime.now(pytz.timezone(TIMEZONE)).strftime("%A, %B %d, %Y")

    email_body = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
                
                body {{
                    font-family: 'Roboto', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #4CAF50, #45a049);
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                h1 {{
                    margin: 0;
                    font-size: 28px;
                    animation: fadeIn 1s;
                }}
                h2 {{
                    color: #4CAF50;
                    border-bottom: 2px solid #4CAF50;
                    padding-bottom: 10px;
                    margin-top: 30px;
                    font-size: 24px;
                }}
                .content {{
                    padding: 20px;
                }}
                .quote, .challenge, .tip, .fun-fact, .history-fact {{
                    font-style: italic;
                    color: #555;
                    margin: 15px 0;
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-left: 5px solid #4CAF50;
                    border-radius: 5px;
                    transition: transform 0.3s ease;
                }}
                .quote:hover, .challenge:hover, .tip:hover, .fun-fact:hover, .history-fact:hover {{
                    transform: translateX(10px);
                }}
                .weather {{
                    background: linear-gradient(135deg, #3498db, #2980b9);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .weather-icon {{
                    font-size: 64px;
                    margin-right: 15px;
                    display: inline-block;
                    vertical-align: middle;
                }}
                .weather-info {{
                    display: inline-block;
                    vertical-align: middle;
                }}
                .weather-temp {{
                    font-size: 36px;
                    font-weight: bold;
                }}
                .weather-desc {{
                    font-size: 18px;
                    margin-top: 5px;
                }}
                .weather-tip {{
                    margin-top: 10px;
                    font-style: italic;
                }}
                .gif-container {{
                    text-align: center;
                    margin-top: 20px;
                }}
                .gif-container img {{
                    max-width: 100%;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s ease;
                }}
                .gif-container img:hover {{
                    transform: scale(1.05);
                }}
                .news-grid {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin-top: 20px;
                }}
                .news-tile {{
                    background-color: #f0f0f0;
                    padding: 15px;
                    border-radius: 5px;
                    transition: transform 0.3s ease;
                }}
                .news-tile:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                }}
                .news-tile h3 {{
                    font-size: 16px;
                    margin-top: 0;
                }}
                .news-tile a {{
                    color: #4CAF50;
                    text-decoration: none;
                }}
                .crossword-container {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-between;
                    margin-top: 20px;
                }}
                .crossword {{
                    background-color: #e9e9e9;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    width: calc(50% - 10px);
                }}
                .crossword-puzzle {{
                    font-family: monospace;
                    font-size: 18px;
                    letter-spacing: 3px;
                }}
                .reveal-btn {{
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    cursor: pointer;
                    margin-top: 10px;
                }}
                .reveal-btn:hover {{
                    background-color: #45a049;
                }}
                .historical-events {{
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-radius: 5px;
                    margin-top: 20px;
                }}
                .historical-events h3 {{
                    color: #4CAF50;
                    margin-top: 0;
                }}
                .footer {{
                    background-color: #333;
                    color: white;
                    text-align: center;
                    padding: 10px;
                    font-size: 0.9em;
                }}
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
                @keyframes slideIn {{
                    from {{ transform: translateX(-50px); opacity: 0; }}
                    to {{ transform: translateX(0); opacity: 1; }}
                }}
                .animated {{
                    animation: slideIn 0.5s ease-out;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Good Morning, {USER_NAME}! 🌞</h1>
                    <p>Today is {current_date}. It's Day {counter} of your journey!</p>
                </div>
                <div class="content">
                    <div class="weather animated">
                        <div class="weather-icon">{weather_icon}</div>
                        <div class="weather-info">
                            <div class="weather-temp">{weather.split(',')[0]}</div>
                            <div class="weather-desc">{weather_description}</div>
                        </div>
                        <div class="weather-tip">{weather_tip}</div>
                    </div>
                    
                    <h2>Motivational Quote</h2>
                    <p class="quote animated">{quote}</p>
                    
                    <h2>This Day in History</h2>
                    <p class="history-fact animated">{history_fact}</p>
                    
                    <h2>AI News</h2>
                    <div class="news-grid">
                        <div class="news-tile">
                            <h3>Artificial Intelligence</h3>
                            {''.join(f'<p><a href="{article["link"]}">{article["title"]}</a></p>' for article in ai_news)}
                        </div>
                        <div class="news-tile">
                            <h3>AI Development</h3>
                            {''.join(f'<p><a href="{article["link"]}">{article["title"]}</a></p>' for article in ai_dev_news)}
                        </div>
                        <div class="news-tile">
                            <h3>Prompt Engineering</h3>
                            {''.join(f'<p><a href="{article["link"]}">{article["title"]}</a></p>' for article in prompt_eng_news)}
                        </div>
                    </div>
                    
                    <h2>Daily Crosswords</h2>
                    <div class="crossword-container">
                        {''.join(f'''
                        <div class="crossword">
                            <p>Clue: {clue}</p>
                            <p class="crossword-puzzle">{puzzle}</p>
                            <button class="reveal-btn" onclick="this.nextElementSibling.style.display='inline'; this.style.display='none';">Reveal</button>
                            <span style="display:none;">{word}</span>
                        </div>
                        ''' for puzzle, word, clue in crosswords)}
                    </div>
                    
                    <h2>Historical Events</h2>
                    <div class="historical-events">
                        <h3>Births on this day:</h3>
                        <ul>
                           {''.join(f'<li>{birth}</li>' for birth in birthdays)}
                        </ul>
                        <h3>Deaths on this day:</h3>
                        <ul>
                            {''.join(f'<li>{death}</li>' for death in deaths)}
                        </ul>
                    </div>
                    
                    <h2>Fun Fact</h2>
                    <p class="fun-fact animated">{fun_fact}</p>
                    
                    <h2>Your Daily Dose of Motivation</h2>
                    <div class="gif-container">
                        <img src="{gif_url}" alt="Motivational Gif">
                    </div>
                </div>
                <div class="footer">
                    <p>This email is part of your daily motivational series. Keep pushing forward!</p>
                </div>
            </div>
        </body>
    </html>
    """

    logging.info("Email content created.")
    return email_body

if __name__ == "__main__":
    try:
        print("Main execution started.")
        logging.info("Main execution started.")
        
        counter = update_counter()
        print(f"Counter updated: {counter}")

        subject = f"Day {counter}: Your Daily Dose of Motivation and Information 🌟"
        to_email = TEST_SEND_TO
        html_content = create_email_content(counter)

        print("Sending email.")
        logging.info("Sending email.")
        send_email(subject, to_email, html_content)
        print("Email sent successfully.")
        logging.info("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
        print(f"Check the log file for more details: {log_filename}")
    finally:
        print("Script execution completed.")
        logging.info("Script execution completed.")