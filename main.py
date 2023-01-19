import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

email_sender = os.getenv("EMAIL_SENDER")
password = os.getenv("PASSWORD")

to = "lucianoaf8@gmail.com"
subject = "Test Email with HTML and styling"

# Create the HTML body
html = """
<html>
  <body>
    <h1 style="color: blue;">This is a test email sent from Python script</h1>
    <p>This is a <b>test</b> email.</p>
  </body>
</html>
"""

smtp_server = "smtp.gmail.com"
port = 587

# Create the message
message = MIMEMultipart()
message["From"] = email_sender
message["To"] = to
message["Subject"] = subject

# Add the HTML to the body of the message
message.attach(MIMEText(html, "html"))

# Connect to the server
server = smtplib.SMTP(smtp_server, port)

# Start the server
server.starttls()

# Login
server.login(email_sender, password)

# Send the email
server.sendmail(email_sender, to, message.as_string())

# Close the server
server.quit()

print("Email sent successfully!")
