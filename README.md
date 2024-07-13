# DAILY_EMAIL

This project generates and sends a daily email containing motivational quotes, weather updates, historical events, news, and more. The email content is dynamically generated using various APIs and is styled for compatibility across email clients.

## Folder Structure
```
DAILY_EMAIL/
│
├── pycache/
│
├── data_files/
│ ├── counter.txt
│ ├── email_preview.html
│ └── keys.xlsx
│
├── logs/
│
├── static/
│ └── css/
│ └── email_style.css
│
├── templates/
│ └── email_template.html
│
├── utils/
│ ├── pycache/
│ │ ├── logging_setup.cpython-312.pyc
│ │ ├── send_email.cpython-312.pyc
│ │ └── utils.cpython-312.pyc
│ │
│ ├── logging_setup.py
│ ├── send_email.py
│ └── utils.py
│
├── .env
├── .gitignore
├── main copy.py
├── main.py
└── README.md
```

## Overview

### Main Components

1. **main.py**: The main script that orchestrates the generation and sending of the daily email. It initializes logging, loads environment variables, updates the counter, generates the email content, and sends the email.
2. **utils/logging_setup.py**: Sets up the logging configuration for the project, including log rotation and customizable log levels and formats.
3. **utils/send_email.py**: Contains the function to send the email using Gmail's SMTP server. It supports adding attachments and logs the process.
4. **utils/utils.py**: Defines utility functions to fetch data from various APIs, manage the counter, read files, and inline CSS for the email content.
5. **templates/email_template.html**: The HTML template for the email content, dynamically populated with data using the Jinja2 templating engine.
6. **static/css/email_style.css**: The CSS file for styling the email content.

### Features

- **Logging**: Centralized logging setup that includes log rotation, configurable log levels and formats, and dynamic inclusion of the script name in log messages.
- **Environment Variables**: Loads sensitive information and configuration settings from a `.env` file.
- **Dynamic Content Generation**: Fetches data from various APIs to include in the email, such as motivational quotes, weather updates, historical events, and news.
- **Email Sending**: Uses Gmail's SMTP server to send the generated email, with support for attachments.
- **Responsive Design**: The email content is styled to be compatible across different email clients.

## Setup

### Prerequisites

- Python 3.12 or higher
- Required Python packages (listed in `requirements.txt` or install via pip)
- A `.env` file with the necessary environment variables

### Environment Variables

Create a `.env` file in the root directory with the following variables:
```
GMAIL_USER=your_gmail_username
GMAIL_PASSWORD=your_gmail_password
USER_NAME=Your_Name
USER_CITY=Your_City
USER_COUNTRY=Your_Country
TIMEZONE=Your_Timezone
TEST_SEND_TO=recipient_email@example.com
GIPHY_API_KEY=your_giphy_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

### Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/your_username/DAILY_EMAIL.git
   cd DAILY_EMAIL
   ```

#### Install Dependencies:
```
pip install -r requirements.txt
```

#### Run the Script:

```
python main.py
```

Folder Details
--------------

-   **pycache/**: Contains compiled Python files.
-   **data_files/**: Stores data files such as the counter, email preview, and keys.
    -   **counter.txt**: Keeps track of the daily email count.
    -   **email_preview.html**: Stores a preview of the generated email content.
    -   **keys.xlsx**: (Optional) Additional data file for key storage.
-   **logs/**: Stores log files generated during the execution of the script.
-   **static/css/**: Contains the CSS file for styling the email content.
    -   **email_style.css**: Stylesheet for the email content.
-   **templates/**: Contains the HTML template for the email content.
    -   **email_template.html**: HTML template for the email, populated with dynamic content.
-   **utils/**: Contains utility scripts for logging setup, email sending, and other helper functions.
    -   **logging_setup.py**: Sets up logging for the project.
    -   **send_email.py**: Contains the email sending function.
    -   **utils.py**: Defines various utility functions.

#### Example Usage

To generate and send the daily email, ensure the `main.py` script is properly configured and run it:


`python main.py`

The script will log its progress and any errors in the `logs/` directory, and the generated email preview will be saved in `data_files/email_preview.html`.

Contributing
------------

Feel free to submit issues, fork the repository, and send pull requests. For major changes, please open an issue first to discuss what you would like to change.

License
-------

This project is licensed under the MIT License.