from dotenv import load_dotenv
import requests
import os
from send_email import send_email

# Load environment variables from .env file
load_dotenv()

# Path to the file storing the counter
COUNTER_FILE = 'counter.txt'
TEST_SEND_TO = os.getenv("TEST_SEND_TO")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
QUOTE_API_KEY = os.getenv("QUOTE_API_KEY")

def get_gif():
    response = requests.get(f"https://api.giphy.com/v1/gifs/random?tag=celebrate&api_key={GIPHY_API_KEY}")
    gif_data = response.json()['data']
    gif_url = gif_data['images']['original']['url']
    return gif_url

def get_quote():
    response = requests.get("https://api.quotable.io/random?tags=philosophy")
    quote_data = response.json()
    quote = f"{quote_data['content']} - {quote_data['author']}"
    return quote
  
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

    return email_body

if __name__ == "__main__":
    # Update the counter once and use it consistently
    counter = update_counter()

    # Email details
    subject = f"EXTRA! EXTRA! EXTRA! {counter} days going strong 🥳"
    to_email = TEST_SEND_TO
    html_content = create_email_content()

    # Send the email
    send_email(subject, to_email, html_content)
