import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
from dotenv import load_dotenv
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()

def send_email(subject: str, to_email: str, html: str, attachments: Optional[List[str]] = None) -> None:
    # Load environment variables
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")
    display_name = os.getenv("DISPLAY_NAME")

    # Debugging: Print environment variables
    print(f"GMAIL_USER: {gmail_user}")
    print(f"GMAIL_PASSWORD: {'*' * len(gmail_password)}")  # Mask the password
    print(f"DISPLAY_NAME: {display_name}")

    # Create the MIME object
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = formataddr((display_name, gmail_user))
    msg['To'] = to_email

    # Debugging: Print email details
    print(f"Email Subject: {subject}")
    print(f"Email From: {msg['From']}")
    print(f"Email To: {msg['To']}")

    # Attach the HTML content
    mime_text = MIMEText(html, 'html')
    msg.attach(mime_text)

    # Attach files
    if attachments:
        for file_path in attachments:
            try:
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(file_path)}',
                )
                msg.attach(part)
                print(f"Attached file: {file_path}")
            except Exception as e:
                print(f"Failed to attach file {file_path}: {e}")

    # Connect to Gmail's SMTP server and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            print("Connecting to SMTP server...")
            server.login(gmail_user, gmail_password)
            print("Login successful.")
            server.sendmail(gmail_user, to_email, msg.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Error: SMTP Authentication failed.")
    except smtplib.SMTPRecipientsRefused:
        print("Error: The recipient's address was refused.")
    except smtplib.SMTPSenderRefused:
        print("Error: The sender's address was refused.")
    except smtplib.SMTPDataError:
        print("Error: The SMTP server refused to accept the message data.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Test the function
    test_subject = "Test Email"
    test_to_email = "lucianoaf8@gmail.com"
    test_html = "<h1>This is a test email.</h1><p>Sent from Python script.</p>"
    test_attachments = []# ["path/to/attachment1.pdf", "path/to/attachment2.jpg"]  # Replace with actual file paths
    send_email(test_subject, test_to_email, test_html, test_attachments)
