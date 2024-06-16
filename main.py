import os
import requests
from dotenv import load_dotenv
import logging
from datetime import datetime
from send_email import send_email

# Load environment variables from .env file
load_dotenv()

# Path to the file storing the counter
COUNTER_FILE = 'counter.txt'
TEST_SEND_TO = os.getenv("TEST_SEND_TO")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

# Set up logging
log_folder = "/logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_filename = os.path.join(log_folder, f"email_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(message)s')

def get_gif():
    logging.info("Fetching GIF of the day.")
    response = requests.get(f"https://api.giphy.com/v1/gifs/random?tag=celebrate&api_key={GIPHY_API_KEY}")
    gif_data = response.json()['data']
    gif_url = gif_data['images']['original']['url']
    logging.info(f"GIF URL: {gif_url}")
    return gif_url

def get_quote():
    logging.info("Fetching quote of the day.")
    response = requests.get("https://api.quotable.io/random?tags=philosophy")
    quote_data = response.json()
    quote = f"{quote_data['content']} - {quote_data['author']}"
    logging.info(f"Quote: {quote}")
    return quote
  
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

def create_email_content():
    logging.info("Creating email content.")
    # Get the gif of the day
    gif_url = get_gif()

    # Get the quote of the day
    quote = get_quote()

    # Create the email content
    email_body = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                h1 {{
                    color: #4CAF50;
                }}
                .quote {{
                    font-style: italic;
                    color: #555;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 0.9em;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <h2>Gif of the Day</h2>
            <img src="{gif_url}" alt="Gif of the day" style="max-width:100%;height:auto;">
            <h2>Quote of the Day</h2>
            <p class="quote">{quote}</p>
            <div class="footer">
                <p>This email is part of your daily motivational series.</p>
            </div>
        </body>
    </html>
    """

    logging.info("Email content created.")
    return email_body

if __name__ == "__main__":
    try:
        logging.info("Script started.")
        
        # Update the counter once and use it consistently
        counter = update_counter()

        # Email details
        subject = f"EXTRA! EXTRA! EXTRA! {counter} days going strong 🥳"
        to_email = TEST_SEND_TO
        html_content = create_email_content()

        # Send the email
        logging.info("Sending email.")
        send_email(subject, to_email, html_content)
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
