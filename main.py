import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

def send_email(to_email, subject, body):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    # Send the email
    server.send_message(msg)
    server.quit()

    print(f"Email sent to {to_email}")

if __name__ == "__main__":
    # Test the function
    test_to_email = "example@example.com"
    test_subject = "Test Email"
    test_body = "This is a test email."
    send_email(test_to_email, test_subject, test_body)
