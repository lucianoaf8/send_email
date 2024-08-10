# email_sender.py

"""
This script provides functionality to send emails with optional attachments using Gmail's SMTP server.
It leverages environment variables for configuration and supports logging to record the status and
errors encountered during the email sending process.

Features:
1. **Environment Variables**: Uses the `dotenv` package to load configuration such as Gmail user,
   password, and display name from a `.env` file.

2. **Email Composition**: Constructs an email with a subject, recipient, and HTML content using the
   `email.mime` package.

3. **Attachments**: Supports adding multiple attachments to the email. Files are read and attached
   using the `MIMEBase` class and encoded in base64.

4. **Logging**: Utilizes the logging configuration set up by `utils.logging_setup` to log information
   and errors, including details about attached files and email sending status.

5. **SMTP Connection**: Establishes a secure connection to Gmail's SMTP server using `smtplib.SMTP_SSL`
   to send the email.

Usage:
- Ensure that environment variables for Gmail user, password, and display name are set in a `.env` file.
- Import the `send_email` function from this script.
- Call `send_email` with the required parameters for subject, recipient email, and HTML content.
- Optionally, provide a list of file paths to attach to the email.

Example:
```
from email_sender import send_email

subject = "Test Email"
to_email = "example@example.com"
html_content = "<h1>This is a test email.</h1><p>Sent from Python script.</p>"
attachments = ["path/to/attachment1.pdf", "path/to/attachment2.jpg"] # Replace with actual file paths

send_email(subject, to_email, html_content, attachments)
```

This example sends an email with the specified subject and HTML content to the recipient's email address,
attaching the specified files.
"""

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
from dotenv import load_dotenv
from typing import List, Optional
from utils.logging_setup import setup_logging

# Load environment variables from .env file
load_dotenv()

def send_email(subject: str, to_email: str, html: str, attachments: Optional[List[str]] = None) -> None:
    """
    Send an email with the specified subject, recipient, and HTML content.
    Optionally attach files.

    Args:
        subject (str): Subject of the email.
        to_email (str): Recipient's email address.
        html (str): HTML content of the email.
        attachments (Optional[List[str]]): List of file paths to attach.
    """
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
                logging.info(f"Attached file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to attach file {file_path}: {e}")

    # Connect to Gmail's SMTP server and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            logging.info("Logging in...")
            server.login(gmail_user, gmail_password)
            logging.info("Sending email...")
            server.sendmail(gmail_user, to_email, msg.as_string())
            logging.info("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        logging.error("Error: SMTP Authentication failed.")
    except smtplib.SMTPRecipientsRefused:
        logging.error("Error: The recipient's address was refused.")
    except smtplib.SMTPSenderRefused:
        logging.error("Error: The sender's address was refused.")
    except smtplib.SMTPDataError:
        logging.error("Error: The SMTP server refused to accept the message data.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Test the function
    test_subject = "Test Email"
    test_to_email = "lucianoaf8@gmail.com"
    test_html = "<h1>This is a test email.</h1><p>Sent from Python script.</p>"
    test_attachments = []  # ["path/to/attachment1.pdf", "path/to/attachment2.jpg"]  # Replace with actual file paths
    send_email(test_subject, test_to_email, test_html, test_attachments)
