# Create new directories
New-Item -ItemType Directory -Force -Path app, app/services, app/utils, app/templates/components, static/css/components, tests

# Move existing files to new locations
Move-Item -Path main.py -Destination app/main.py -Force
Move-Item -Path utils/logging_setup.py -Destination app/utils/logging_setup.py -Force
Move-Item -Path utils/send_email.py -Destination app/services/email_service.py -Force
Move-Item -Path templates/email_template.html -Destination app/templates/email_template.html -Force
Move-Item -Path templates/*.html -Destination app/templates/components/ -Force
Move-Item -Path static/css/*.css -Destination static/css/components/ -Force -Exclude email_style.css
Move-Item -Path static/css/email_style.css -Destination static/css/email_style.css -Force

# Create new files
New-Item -ItemType File -Force -Path app/__init__.py, app/config.py, app/services/__init__.py, app/utils/__init__.py, app/utils/helpers.py, tests/__init__.py, tests/test_weather_service.py, tests/test_news_service.py, tests/test_quote_service.py, tests/test_history_service.py, tests/test_fun_fact_service.py, tests/test_email_service.py, preview_server.py, requirements.txt

# Create new service files
"weather_service.py", "news_service.py", "quote_service.py", "history_service.py", "fun_fact_service.py" | ForEach-Object {
    New-Item -ItemType File -Force -Path "app/services/$_"
}

# Move content from utils.py to respective service files
$utils_content = Get-Content -Path utils/utils.py -Raw
$utils_content | Out-File -FilePath app/utils/helpers.py -Encoding utf8

# Delete old directories and files
Remove-Item -Recurse -Force -Path utils, templates
Remove-Item -Force -Path README.md

# Create new README.md
@"
# Daily Email Project

This project sends daily emails with personalized content including weather forecasts, news updates, and motivational quotes.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys and email credentials
4. Run the main script: `python -m app.main`

## Preview Email Template

To preview the email template:

1. Run the preview server: `python preview_server.py`
2. Open a web browser and navigate to `http://localhost:5000`

## Running Tests

Run tests using pytest: `pytest tests/`

## Project Structure

- `app/`: Main application code
  - `services/`: Individual service modules
  - `templates/`: Email templates
  - `utils/`: Utility functions
- `static/`: Static assets (CSS)
- `tests/`: Unit tests
- `preview_server.py`: Flask server for previewing email templates

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
"@ | Out-File -FilePath README.md -Encoding utf8

# Print completion message
Write-Host "Project structure has been updated successfully!" -ForegroundColor Green