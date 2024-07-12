import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
from datetime import datetime
import pytz
from send_email import send_email
import random
import jinja2
import cssutils
import io
from utils import handle_api_error, compress_image, ab_test, get_fallback_data, update_fallback_data, APIError


# Suppress cssutils logging
cssutils.log.setLevel(logging.CRITICAL)

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
    try:
        response = requests.get(f"https://api.giphy.com/v1/gifs/random?tag=motivational&api_key={GIPHY_API_KEY}")
        response.raise_for_status()
        gif_data = response.json()['data']
        gif_url = gif_data['images']['original']['url']
        compressed_gif = compress_image(gif_url)
        update_fallback_data('gif', compressed_gif)
        logging.info(f"GIF fetched and compressed successfully")
        return compressed_gif
    except requests.RequestException as e:
        handle_api_error("Giphy", e)
        return get_fallback_data('gif')
    
def get_quote():
    logging.info("Fetching quote of the day.")
    try:
        response = requests.get("https://api.quotable.io/random?tags=inspirational")
        response.raise_for_status()
        quote_data = response.json()
        quote = f"{quote_data['content']} - {quote_data['author']}"
        update_fallback_data('quote', quote)
        logging.info(f"Quote fetched: {quote}")
        return quote
    except requests.RequestException as e:
        handle_api_error("Quotable", e)
        return get_fallback_data('quote')

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

def get_this_day_in_history():
    logging.info("Fetching this day in history.")
    today = datetime.now()
    month, day = today.month, today.day
    response = requests.get(f"https://history.muffinlabs.com/date/{month}/{day}")
    data = response.json()
    event = data['data']['Events'][0]  # Get the first event
    return f"{event['year']}: {event['text']}"

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
    
    # Add original CSS in <style> tag for local viewing
    style_tag = soup.new_tag('style')
    style_tag.string = css
    soup.head.append(style_tag)
    
    return str(soup)

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
        
        ai_news = fetch_news("Artificial Intelligence")
        ai_dev_news = fetch_news("AI Development")
        prompt_eng_news = fetch_news("Prompt Engineering")
        
        birthdays = get_historical_birthdays()
        deaths = get_historical_deaths()
        
        current_date = datetime.now(pytz.timezone(TIMEZONE)).strftime("%A, %B %d, %Y")
        
        # A/B testing for quote placement
        quote_placement = ab_test('top', 'bottom')
        
        # Read the HTML template
        template_content = read_file('email_template.html')

        # Read the CSS content
        css_content = read_file('email_style.css')

        # Create Jinja2 environment and template
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = env.from_string(template_content)
        
        # Render the template with the data
        html_content = template.render(
            USER_NAME=USER_NAME,
            current_date=current_date,
            counter=counter,
            weather=weather,
            weather_icon=weather_icon,
            weather_description=weather_description,
            weather_tip=weather_tip,
            quote=quote,
            quote_placement=quote_placement,
            history_fact=history_fact,
            ai_news=ai_news,
            ai_dev_news=ai_dev_news,
            prompt_eng_news=prompt_eng_news,
            birthdays=birthdays,
            deaths=deaths,
            fun_fact=fun_fact,
            gif_url=gif_url
        )
        
        # Inline the CSS
        final_html = inline_css(html_content, css_content)
        
        # Save the final HTML to a file for local viewing
        with io.open('email_preview.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        logging.info("Email content created with inlined CSS and saved for local viewing.")
        return final_html
    
    except Exception as e:
        print(f"Error while creating content: {e}")
        logging.error(f"Error while creating content: {e}")
        raise

if __name__ == "__main__":
    try:
        print("Main execution started.")
        logging.info("Main execution started.")
        
        counter = update_counter()
        print(f"Counter updated: {counter}")

        subject_a = f"Day {counter}: Your Daily Dose of Motivation and Information 🌟"
        subject_b = f"Day {counter}: Inspire Your Day with Facts and Fun 🎉"
        subject = ab_test(subject_a, subject_b)

        to_email = TEST_SEND_TO
        html_content = create_email_content(counter)

        print("Sending email.")
        logging.info("Sending email.")
        send_email(subject, to_email, html_content, ab_test_metadata={'subject': subject})
        print("Email sent successfully.")
        logging.info("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
        print(f"Check the log file for more details: {log_filename}")
    finally:
        print("Script execution completed.")
        logging.info("Script execution completed.")