# utils/utils.py

"""
This script defines utility functions used by the main script to fetch data and perform various tasks
required for generating the daily email. It includes functions for fetching GIFs, quotes, weather,
historical events, news, and more. Additionally, it provides functions for handling the counter, reading
files, and inlining CSS.

Features:
1. **GIF Fetching**: Fetches a motivational GIF of the day from the Giphy API.
   - `get_gif()`: Fetches and returns the URL of a random motivational GIF.

2. **Quote Fetching**: Fetches an inspirational quote of the day from the Quotable API.
   - `get_quote()`: Fetches and returns a random inspirational quote.

3. **Weather Information**: Fetches the current weather information for a specified city.
   - `get_weather()`: Fetches and returns the current temperature and weather description.
   - `get_weather_icon(description)`: Returns a corresponding weather icon for the given description.
   - `get_weather_tip(description)`: Provides a weather tip based on the weather description.

4. **Historical Data**: Fetches historical events, births, and deaths that occurred on the current day.
   - `get_this_day_in_history()`: Fetches and returns a historical event for the current day.
   - `get_historical_birthdays()`: Fetches and returns a list of notable births on the current day.
   - `get_historical_deaths()`: Fetches and returns a list of notable deaths on the current day.

5. **News Fetching**: Fetches the latest news articles on specified topics from Google News.
   - `fetch_news(topic, num_articles=3)`: Fetches and returns a list of news articles for the given topic.

6. **Fun Fact**: Fetches a random fun fact from the Useless Facts API.
   - `get_fun_fact()`: Fetches and returns a random fun fact.

7. **Counter Management**: Manages a counter stored in a file to keep track of daily emails.
   - `update_counter()`: Updates and returns the current counter value.

8. **File Reading**: Reads the content of a specified file.
   - `read_file(filename)`: Reads and returns the content of a file.

9. **CSS Inlining**: Inlines CSS styles into HTML content for better email compatibility.
   - `inline_css(html, css)`: Inlines the CSS styles into the given HTML content.

Usage:
- Import the required functions from this script.
- Call the functions as needed to fetch data, manage the counter, read files, and inline CSS.

Example:
```
from utils.utils import get_gif, get_quote, get_weather, update_counter, read_file, inline_css

gif_url = get_gif()
quote = get_quote()
weather = get_weather()
counter = update_counter()
html_template = read_file('templates/email_template.html')
css_styles = read_file('static/css/email_style.css')
final_html = inline_css(html_template, css_styles)
```

This example demonstrates how to fetch various data, update the counter, read files, and inline CSS.
"""

import os
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import cssutils


# Suppress cssutils logging
cssutils.log.setLevel(logging.CRITICAL)

COUNTER_FILE = 'data_files/counter.txt'

def get_gif():
    logging.info("Fetching GIF of the day.")
    response = requests.get(f"https://api.giphy.com/v1/gifs/random?tag=motivational&api_key={os.getenv('GIPHY_API_KEY')}")
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
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={os.getenv('USER_CITY')},{os.getenv('USER_COUNTRY')}&appid={os.getenv('OPENWEATHER_API_KEY')}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        if 'main' not in weather_data:
            logging.error(f"Unexpected API response: {weather_data}")
            return "Weather data unavailable"
        
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        result = f"{temp:.1f}°C, {description}"
        logging.info(f"Weather fetched successfully: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather: {e}")
        return "Weather data unavailable"
    except KeyError as e:
        logging.error(f"Error parsing weather data: {e}")
        return "Weather data unavailable"
    except Exception as e:
        logging.error(f"Unexpected error in get_weather: {e}")
        return "Weather data unavailable"

def get_weather_icon(description):
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
    return weather_icons.get(description.lower(), '🌡️')

def get_weather_tip(description):
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

def get_this_day_in_history():
    logging.info("Fetching this day in history.")
    today = datetime.now()
    month, day = today.month, today.day
    response = requests.get(f"https://history.muffinlabs.com/date/{month}/{day}")
    data = response.json()
    event = data['data']['Events'][0]
    return f"{event['year']}: {event['text']}"

def fetch_news(topic, num_articles=3):
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

def get_historical_birthdays():
    today = datetime.now()
    month, day = today.month, today.day
    url = f"https://history.muffinlabs.com/date/{month}/{day}"
    response = requests.get(url)
    data = response.json()
    births = data['data']['Births'][:3]
    return [f"{person['year']}: {person['text']}" for person in births]

def get_historical_deaths():
    today = datetime.now()
    month, day = today.month, today.day
    url = f"https://history.muffinlabs.com/date/{month}/{day}"
    response = requests.get(url)
    data = response.json()
    deaths = data['data']['Deaths'][:3]
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

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def inline_css(html, css):
    soup = BeautifulSoup(html, 'html.parser')
    style = cssutils.parseString(css)
    
    for rule in style:
        if rule.type == rule.STYLE_RULE:
            for selector in rule.selectorList:
                for tag in soup.select(selector.selectorText):
                    if not tag.get('style'):
                        tag['style'] = ''
                    tag['style'] += f'{rule.style.cssText};'
    
    style_tag = soup.new_tag('style')
    style_tag.string = css
    soup.head.append(style_tag)
    
    return str(soup)
