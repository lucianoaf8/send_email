# main.py

"""
This script serves as the main entry point for generating and sending a daily email that includes various
informative and motivational content. The script coordinates fetching data, generating HTML content,
and sending the email using pre-defined utility functions and environment configurations.

Features:
1. **Logging Initialization**: Sets up logging using a centralized configuration to ensure all log messages
   are captured in a single log file with the script name included in each message.

2. **Environment Variables**: Loads environment variables from a `.env` file using the `dotenv` package to
   configure the script, including email credentials and user-specific settings.

3. **Email Content Creation**: Generates the email content dynamically using various utility functions to
   fetch data such as weather information, quotes, historical facts, and news. The content is then rendered
   using a Jinja2 template and inlined with CSS for styling.

4. **Error Handling**: Includes comprehensive error handling to log any issues that occur during the content
   creation or email sending process, ensuring that issues can be easily diagnosed from the log file.

5. **Email Sending**: Sends the generated email using Gmail's SMTP server, with the option to specify a recipient
   through environment variables.

Usage:
- Ensure that environment variables for Gmail user, password, and recipient email are set in a `.env` file.
- Run the script as the main module to generate and send the daily email.

Example:
```
if name == "main":
try:
counter = update_counter()
subject = f"Day {counter}: Your Daily Dose of Motivation and Information 🌟"
to_email = os.getenv("TEST_SEND_TO")
html_content = create_email_content(counter)
send_email(subject, to_email, html_content)
except Exception as e:
logging.error(f"An error occurred: {e}")
logging.info(f"Check the log file for more details: {log_filename}")
finally:
logging.info("Script execution completed.")
```

This example initializes the counter, generates the email content, and sends the email while handling
any exceptions that occur during the process.
"""

import os
import logging
import traceback
from dotenv import load_dotenv
from datetime import datetime
from utils.logging_setup import setup_logging
from utils.send_email import send_email
from utils.utils import get_gif, get_quote, get_weather, get_weather_icon, get_weather_tip, get_this_day_in_history, fetch_news, get_historical_birthdays, get_historical_deaths, get_fun_fact, read_file, get_email_recipients, update_recipient_counter
import io
import pytz
import jinja2
from premailer import Premailer
import pandas as pd

# Set up logging with the script name
log_filename = setup_logging(log_folder='logs', log_level=logging.INFO, log_format='%(script_name)s - %(asctime)s %(message)s')
logging.info("Script started.")

# Load environment variables from .env file
load_dotenv()
logging.info("Environment variables loaded.")

def load_keys():
    try:
        return pd.read_excel('data_files/keys.xlsx')
    except Exception as e:
        logging.error(f"Error loading keys: {e}")
        return pd.DataFrame()
    
def create_email_content(counter, username, interests, city, country):
    logging.info("Creating email content.")
    try:
        gif_url = get_gif()
        quote = get_quote()
        weather = get_weather(city, country)
        weather_description = weather.split(',')[-1].strip()
        weather_icon = get_weather_icon(weather_description)
        weather_tip = get_weather_tip(weather_description)
        weather_class = f"weather-widget__{weather_description.lower().replace(' ', '-')}"
        history_fact = get_this_day_in_history()
        fun_fact = get_fun_fact()
        
        # Fetch news for each interest
        news_by_topic = {}
        for topic in interests.split(','):
            topic = topic.strip()
            news_by_topic[topic] = fetch_news(topic)
        
        birthdays = get_historical_birthdays()
        deaths = get_historical_deaths()
        
        current_date = datetime.now(pytz.timezone(os.getenv('TIMEZONE', 'UTC'))).strftime("%A, %B %d, %Y")
        
        # Set up the Jinja2 environment with the correct template loader
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        template = env.get_template('email_template.html')
        
        html_content = template.render(
            USER_NAME=username,
            current_date=current_date,
            counter=counter,
            weather=weather,
            weather_icon=weather_icon,
            weather_description=weather_description,
            weather_tip=weather_tip,
            weather_class=weather_class,
            city=city,
            country=country,
            quote=quote,
            history_fact=history_fact,
            news_by_topic=news_by_topic,
            birthdays=birthdays,
            deaths=deaths,
            fun_fact=fun_fact,
            gif_url=gif_url
        )
        
        # Read and concatenate all CSS files
        css_files = [
            'static/css/general.css',
            'static/css/container.css',
            'static/css/header.css',
            'static/css/content.css',
            'static/css/weather_widget.css',
            'static/css/sections.css',
            'static/css/gif_container.css',
            'static/css/news_grid.css',
            'static/css/historical_events.css',
            'static/css/footer.css'
        ]
        css_content = ''
        for css_file in css_files:
            css_content += read_file(css_file) + '\n'
        
        # Remove <link> tags from the HTML content
        html_content = html_content.replace('<link rel="stylesheet" href="static/css/email_style.css">', '')

        # Inline the CSS using Premailer
        premailer = Premailer(html=html_content, css_text=css_content)
        final_html = premailer.transform()
        
        with io.open('data_files/email_preview.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        logging.info("Email content created with inlined CSS and saved for local viewing.")
        return final_html
    except jinja2.exceptions.TemplateNotFound as e:
        logging.error(f"Template not found: {e}")
        logging.error(traceback.format_exc())
        raise
    except Exception as e:
        logging.error(f"Error while creating content: {e}")
        logging.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    try:
        keys_df = load_keys()
        email_recipients = get_email_recipients(keys_df)
        
        for username, email, counter, interests, city, country in email_recipients:
            subject = f"Day {counter}: Your Daily Dose of Motivation and Information 🌟"
            html_content = create_email_content(counter, username, interests, city, country)

            send_email(subject, email, html_content)
            update_recipient_counter(keys_df, email)
            
            logging.info(f"Email sent to {username} at {email}")

        # Save updated keys file
        keys_df.to_excel('data_files/keys.xlsx', index=False)
        logging.info("Keys file updated with new counters.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error(traceback.format_exc())
        logging.info(f"Check the log file for more details: {log_filename}")
    finally:
        logging.info("Script execution completed.")