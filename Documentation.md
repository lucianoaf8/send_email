README.md:



# Daily Motivational Email Generator

## Overview

This project is an automated system that generates and sends daily motivational emails. It combines various elements such as weather forecasts, inspirational quotes, historical events, news updates, and more to create personalized, engaging daily emails for the recipient.

## Features

- Daily counter to track the recipient's journey

- Current weather information and tips

- Motivational quote of the day

- Historical events, births, and deaths on the current date

- Fun fact of the day

- Motivational GIF

- Daily challenge

- Curated news articles on AI, AI Development, and Prompt Engineering

- Responsive email design with inline CSS for better compatibility across email clients

## Project Structure

```

DAILY_EMAIL/

├── data_files/           # Stores data files used by the script

├── logs/                 # Directory for log files

├── static/               # Static files (CSS)

│   └── css/

├── templates/            # HTML templates for email components

├── utils/                # Utility functions and modules

├── .env                  # Environment variables (not in version control)

├── .gitignore            # Git ignore file

├── main.py               # Main script to generate and send emails

└── README.md             # This file

```

## Prerequisites

- Python 3.7+

- Required Python packages (install via `pip install -r requirements.txt`):

  - requests

  - beautifulsoup4

  - python-dotenv

  - jinja2

  - premailer

  - cssutils

## Setup

1\. Clone the repository:

   ```

   git clone https://github.com/yourusername/daily-motivational-email.git

   cd daily-motivational-email

   ```

2\. Install the required packages:

   ```

   pip install -r requirements.txt

   ```

3\. Create a `.env` file in the project root and add the following variables:

   ```

   GMAIL_USER=your_email@gmail.com

   GMAIL_PASSWORD=your_app_password

   DISPLAY_NAME=Your Name

   TEST_SEND_TO=recipient@example.com

   GIPHY_API_KEY=your_giphy_api_key

   OPENWEATHER_API_KEY=your_openweather_api_key

   USER_CITY=YourCity

   USER_COUNTRY=YourCountry

   TIMEZONE=Your/Timezone

   ```

   Note: For Gmail, you'll need to use an App Password. Follow [Google's instructions](https://support.google.com/accounts/answer/185833?hl=en) to set this up.

4\. Ensure the `data_files` directory contains the `counter.txt` file. If not, create it with an initial value of 0.

## Usage

Run the main script to generate and send the daily email:

```

python main.py

```

The script will:

1\. Update the daily counter

2\. Fetch all required data (weather, quote, news, etc.)

3\. Generate the email content

4\. Send the email to the specified recipient

## Customization

- Modify HTML templates in the `templates/` directory to change the email layout and content.

- Adjust CSS styles in the `static/css/` directory to customize the email appearance.

- Update the `utils/utils.py` file to add or modify data fetching functions.

## Logging

Logs are stored in the `logs/` directory. Check these logs for script execution details and any errors that may occur.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

Now, let's provide additional documentation for key components of the project:

1\. main.py



# main.py

This is the main entry point for the Daily Motivational Email Generator. It orchestrates the entire process of creating and sending the daily email.

## Key Functions

- `create_email_content(counter)`: Generates the HTML content for the email, including all dynamic elements.

- `send_email(subject, to_email, html_content)`: Sends the generated email to the specified recipient.

## Process Flow

1\. Initialize logging

2\. Load environment variables

3\. Update the daily counter

4\. Generate email subject

5\. Create email content

6\. Send the email

7\. Handle any exceptions and log errors

## Customization

To modify the email content or add new features:

1\. Update the `create_email_content()` function to include new data or modify existing elements.

2\. Add new utility functions in `utils/utils.py` if needed.

3\. Modify the email template in `templates/email_template.html` to change the overall structure.

```

2\. utils/utils.py



# utils/utils.py

This file contains utility functions used throughout the project for fetching data, managing the counter, and handling file operations.

## Key Functions

- `get_gif()`: Fetches a random motivational GIF from Giphy.

- `get_quote()`: Retrieves an inspirational quote.

- `get_weather()`: Fetches current weather information for the user's location.

- `get_this_day_in_history()`: Retrieves a historical event for the current date.

- `fetch_news(topic, num_articles=3)`: Fetches news articles on a given topic.

- `get_fun_fact()`: Retrieves a random fun fact.

- `update_counter()`: Manages the daily email counter.

- `inline_css(html, css)`: Inlines CSS into the HTML content for better email compatibility.

## Adding New Data Sources

To add a new data source:

1\. Create a new function in this file to fetch the data.

2\. Update the `create_email_content()` function in `main.py` to use the new data.

3\. Modify the email template to include the new information.

```

3\. utils/send_email.py



# utils/send_email.py

This module handles the email sending functionality using Gmail's SMTP server.

## Key Function

- `send_email(subject, to_email, html, attachments=None)`: Sends an email with the specified subject, recipient, HTML content, and optional attachments.

## Security Note

This script uses environment variables to store sensitive information like email credentials. Ensure that the `.env` file is not committed to version control and is properly secured.

## Customization

To modify email sending behavior:

1\. Update the `send_email()` function to change SMTP settings or add new features.

2\. Modify error handling to suit your needs.

```

4\. utils/logging_setup.py



# utils/logging_setup.py

This module sets up logging for the entire application, ensuring that all actions and errors are properly recorded.

## Key Function

- `setup_logging(log_folder, log_level, log_format)`: Configures logging with the specified parameters.

## Customization

To modify logging behavior:

1\. Update the `setup_logging()` function to change log rotation settings, formats, or add new handlers.

2\. Modify the `ScriptNameFilter` class to change how the script name is included in log messages.

```

5\. templates/email_template.html



# templates/email_template.html

This is the main template for the daily email. It includes all other template components to create the final email structure.

## Structure

- Head section (CSS imports)

- Container

  - Header

  - Content

    - Weather widget

    - Motivational quote

    - Historical events

    - Fun fact

    - Daily motivation (GIF)

    - Daily challenge

    - News section

  - Footer

## Customization

To modify the email layout:

1\. Update this file to change the overall structure.

2\. Modify individual component templates (e.g., `weather_widget.html`, `news.html`) to change specific sections.

3\. Update corresponding CSS files in `static/css/` to adjust styling.

```

6\. static/css/email_style.css



# static/css/email_style.css

This is the main CSS file that imports all other CSS components for the email styling.

## Imported Stylesheets

- general.css: Base styles and font imports

- container.css: Styles for the main email container

- header.css: Header styles

- content.css: Content area styles

- weather_widget.css: Weather widget specific styles

- sections.css: Styles for various content sections

- gif_container.css: Styles for the motivational GIF container

- news_grid.css: News section grid layout

- historical_events.css: Styles for historical events section

- footer.css: Footer styles

## Customization

To modify email styling:

1\. Update individual CSS files to change specific component styles.

2\. Add new CSS files for new components and import them in this file.

3\. Ensure all styles are inlined properly using the `inline_css()` function in `utils/utils.py`.

```
