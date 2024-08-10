# Daily Email Project

This project sends daily emails with personalized content including weather forecasts, news updates, and motivational quotes.

## Setup

1. Clone the repository
2. Install dependencies: pip install -r requirements.txt
3. Create a .env file with your API keys and email credentials
4. Run the main script: python -m app.main

## Preview Email Template

To preview the email template:

1. Run the preview server: python preview_server.py
2. Open a web browser and navigate to http://localhost:5000

## Running Tests

Run tests using pytest: pytest tests/

## Project Structure

- pp/: Main application code
  - services/: Individual service modules
  - 	emplates/: Email templates
  - utils/: Utility functions
- static/: Static assets (CSS)
- 	ests/: Unit tests
- preview_server.py: Flask server for previewing email templates

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
