# Daily Email Sender

This project sends a daily email with motivational content, including a daily counter, a GIF of the day, and a quote from a famous philosopher. The email is formatted in HTML for better readability.

## Features

- **Daily Counter**: The email subject includes a counter that increases daily.
- **GIF of the Day**: A random GIF tagged with "celebrate" is included in the email body.
- **Quote of the Day**: A daily quote from a famous philosopher is included in the email body.
- **HTML Formatting**: The email content is formatted in HTML for improved aesthetics.

## Prerequisites

- Python 3.8 or later
- A Gmail account for sending emails
- API keys for Giphy and Quotable

## Installation

#### 1. Clone the repository:
```
   git clone https://github.com/yourusername/daily-email-sender.git
   cd daily-email-sender
```

#### 2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### 3. Install the required packages:

```
pip install -r requirements.txt
```

#### 4. Create a .env file in the project directory and add your environment 
variables:

```
GMAIL_USER=your_gmail_user
GMAIL_PASSWORD=your_gmail_password
DISPLAY_NAME=Your Name
TEST_SEND_TO=recipient@example.com
GIPHY_API_KEY=your_giphy_api_key
QUOTE_API_KEY=your_quote_api_key
```

## Usage
Run the main.py script to send a test email:

```
python main.py
```

To schedule the script to run daily, use Windows Task Scheduler or a similar tool on your operating system.

Script Details

```main.py```

- Loads environment variables.
- Updates a daily counter stored in a file (counter.txt).
- Fetches a random GIF of the day from Giphy.
- Fetches a random quote from a philosopher from Quotable.
- Constructs the email content using HTML.
- Sends the email using the send_email function from send_email.py.

```send_email.py```

- Defines a function to send emails using Gmail.
- Uses environment variables for Gmail credentials.
- Supports HTML content and attachments.

### API Usage

#### Giphy
To get a GIF of the day, the script uses the Giphy API:

```
https://api.giphy.com/v1/gifs/random?tag=celebrate&api_key=your_giphy_api_key
```

#### Quotable
To get a quote of the day, the script uses the Quotable API:

```
https://api.quotable.io/random?tags=philosophy
```

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### Acknowledgements
- Giphy API
- Quotable API

