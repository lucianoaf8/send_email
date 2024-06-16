import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_email(subject: str, to_email: str, html: str) -> None:
    # Load environment variables
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")
    display_name = os.getenv("DISPLAY_NAME")

    # Create the MIME object
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = formataddr((display_name, gmail_user))
    msg['To'] = to_email

    # Attach the HTML content
    mime_text = MIMEText(html, 'html')
    msg.attach(mime_text)

    # Connect to Gmail's SMTP server and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test the function
    test_subject = "Test Email"
    test_to_email = "example@example.com"
    test_html = "<h1>This is a test email.</h1><p>Sent from Python script.</p>"
    send_email(test_subject, test_to_email, test_html)
