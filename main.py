# main.py
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
from datetime import datetime
import pytz
import random
import jinja2
import cssutils
import io
from utils.logging_setup import setup_logging
from utils.send_email import send_email

# Suppress cssutils logging
cssutils.log.setLevel(logging.CRITICAL)

log_filename = setup_logging()
logging.info("Script started.")

# Load environment variables from .env file
load_dotenv()
logging.info("Environment variables loaded.")

# Path to the file storing the counter
COUNTER_FILE = 'utils/counter.txt'
TEST_SEND_TO = os.getenv("TEST_SEND_TO")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
USER_NAME = os.getenv("USER_NAME")
USER_CITY = os.getenv("USER_CITY")
USER_COUNTRY = os.getenv("USER_COUNTRY")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
THENEWSAPI_KEY = os.getenv("THENEWSAPI_KEY")

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
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={USER_CITY},{USER_COUNTRY}&appid={OPENWEATHER_API_KEY}&units=metric"
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

def create_email_content(counter):
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
        daily_challenge = "Take a 10-minute walk outside during your break today!"  # Example challenge
        
        ai_news = fetch_news("Artificial Intelligence")
        ai_dev_news = fetch_news("AI Development")
        prompt_eng_news = fetch_news("Prompt Engineering")
        
        birthdays = get_historical_birthdays()
        deaths = get_historical_deaths()
        
        current_date = datetime.now(pytz.timezone(TIMEZONE)).strftime("%A, %B %d, %Y")
        
        template_content = read_file('email_template/email_template.html')
        css_content = read_file('email_template/email_style.css')

        env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = env.from_string(template_content)
        
        html_content = template.render(
            USER_NAME=USER_NAME,
            current_date=current_date,
            counter=counter,
            weather=weather,
            weather_icon=weather_icon,
            weather_description=weather_description,
            weather_tip=weather_tip,
            quote=quote,
            history_fact=history_fact,
            ai_news=ai_news,
            ai_dev_news=ai_dev_news,
            prompt_eng_news=prompt_eng_news,
            birthdays=birthdays,
            deaths=deaths,
            fun_fact=fun_fact,
            gif_url=gif_url,
            daily_challenge=daily_challenge
        )
        
        final_html = inline_css(html_content, css_content)
        
        with io.open('data_files/email_preview.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        logging.info("Email content created with inlined CSS and saved for local viewing.")
        return final_html
    except Exception as e:
        logging.error(f"Error while creating content: {e}")
        raise

if __name__ == "__main__":
    try:
        logging.info("Main execution started.")
        
        counter = update_counter()
        logging.info(f"Counter updated: {counter}")

        subject = f"Day {counter}: Your Daily Dose of Motivation and Information 🌟"
        to_email = TEST_SEND_TO
        html_content = create_email_content(counter)

        logging.info("Sending email.")
        send_email(subject, to_email, html_content)
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.info(f"Check the log file for more details: {log_filename}")
    finally:
        logging.info("Script execution completed.")
