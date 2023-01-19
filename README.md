# Email Sender Script

This script is a Python script that sends an email with HTML and styling using the SMTP (Simple Mail Transfer Protocol) library and the `dotenv` library.

## Features

- The script uses the `os` library to access environment variables set in a `.env` file. These environment variables are used to store the email address of the sender and the password, so that they can be accessed in the script without having to hardcode them.

- The script sets up the recipient's email address, the subject of the email, and the HTML body of the email.

- It also sets up the SMTP server and port to use for sending the email.

- The script creates an email message using the `MIMEMultipart` class, sets the sender, recipient, and subject, and attaches the HTML body of the email to the message.

- It then connects to the SMTP server, starts the server, logs in with the sender's email and password, and sends the email to the recipient.

- Finally, it closes the server and prints a message indicating that the email was sent successfully.

## Usage

1. Make sure to install the following libraries: `smtplib`, `email`, `dotenv` and `python-dotenv`.

2. Create a `.env` file in the same folder of the script and add the following variables:

`EMAIL_SENDER=<your email>`

`PASSWORD=<your email password>`

3. Run the script with python.

4. Check the recipient's email to see if the email was sent successfully.

## Note
It is not recommended to use your main email and password to send emails in a script, it's better to create an app-password in your email provider.

You can customize the script to suit your needs, like changing the HTML body of the email, the recipient, and the subject.
