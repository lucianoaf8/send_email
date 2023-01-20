import os

import requests
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
api_key = os.getenv("SENDGRID_API_KEY")
to_email = "lucianoaf8@gmail.com"
subject = "Test Email with HTML and styling"
html = """
<html>
  <body>
    <h1 style="color: blue;">This is a test email sent from Python script</h1>
    <p>This is a <b>test</b> email.</p>
  </body>
</html>
"""

# Define the endpoint and payload
endpoint = "https://api.sendgrid.com/v3/mail/send"
payload = {
    "personalizations": [
        {
            "to": [
                {
                    "email": to_email
                }
            ],
            "subject": subject
        }
    ],
    "from": {
        "email": "lucianoaf8@gmail.com"
    },
    "content": [
        {
            "type": "text/html",
            "value": html
        }
    ]
}

# Make the request
response = requests.post(endpoint, auth=("Bearer", api_key), json=payload)

# Check the status code
if response.status_code == 202:
    print("Email sent successfully!")
else:
    print(f"Error: {response.content}")
