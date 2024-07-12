import os
import sys
import requests
from dotenv import load_dotenv
import logging
from datetime import datetime
import pytz
from send_email import send_email

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

def get_news_headline():
    logging.info("Fetching news headline.")
    response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_NEWS_API_KEY")
    news_data = response.json()
    headline = news_data['articles'][0]['title']
    return headline

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

def create_email_content(counter):
    print("Creating email content.")
    logging.info("Creating email content.")
    
    try:
        gif_url = get_gif()
        quote = get_quote()
        weather = get_weather()
        history_fact = get_this_day_in_history()
        news_headline = get_news_headline()
        fun_fact = get_fun_fact()
    except Exception as e:
        print(f"Error while fetching content: {e}")
        logging.error(f"Error while fetching content: {e}")
        raise

    # Get the current date in the user's timezone
    current_date = datetime.now(pytz.timezone(TIMEZONE)).strftime("%A, %B %d, %Y")

    email_body = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                h1, h2 {{
                    color: #4CAF50;
                }}
                .quote, .challenge, .tip, .fun-fact {{
                    font-style: italic;
                    color: #555;
                    margin: 15px 0;
                    padding: 10px;
                    background-color: #f0f0f0;
                    border-left: 5px solid #4CAF50;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 0.9em;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <h1>Good Morning, {USER_NAME}!</h1>
            <p>Today is {current_date}. It's Day {counter} of your journey!</p>
            
            <h2>Today's Weather</h2>
            <p>{weather}</p>
            
            <h2>Motivational Quote</h2>
            <p class="quote">{quote}</p>
            
            <h2>This Day in History</h2>
            <p>{history_fact}</p>
            
            <h2>Daily Challenge</h2>
            <p class="challenge">Today, try to do one small act of kindness for someone. It could be as simple as giving a compliment or helping with a task.</p>
            
            <h2>Motivational Tip</h2>
            <p class="tip">Remember to take breaks throughout your day. Short breaks can refresh your mind and boost productivity.</p>
            
            <h2>News Headline</h2>
            <p>{news_headline}</p>
            
            <h2>Fun Fact</h2>
            <p class="fun-fact">{fun_fact}</p>
            
            <h2>Your Daily Dose of Motivation</h2>
            <img src="{gif_url}" alt="Motivational Gif" style="max-width:100%;height:auto;">
            
            <div class="footer">
                <p>This email is part of your daily motivational series. Keep pushing forward!</p>
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