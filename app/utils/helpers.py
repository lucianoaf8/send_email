# utils/utils.py

"""
This script defines utility functions used by the main script to fetch data and perform various tasks
required for generating the daily email. It includes functions for fetching GIFs, quotes, weather,
historical events, news, and more. Additionally, it provides functions for handling the counter, reading
files, and inlining CSS.

Features:
1. **GIF Fetching**: Fetches a motivational GIF of the day from the Giphy API.
   - `get_gif()`: Fetches and returns the URL of a random motivational GIF.

2. **Quote Fetching**: Fetches an inspirational quote of the day from the Quotable API.
   - `get_quote()`: Fetches and returns a random inspirational quote.

3. **Weather Information**: Fetches the current weather information for a specified city.
   - `get_weather()`: Fetches and returns the current temperature and weather description.
   - `get_weather_icon(description)`: Returns a corresponding weather icon for the given description.
   - `get_weather_tip(description)`: Provides a weather tip based on the weather description.

4. **Historical Data**: Fetches historical events, births, and deaths that occurred on the current day.
   - `get_this_day_in_history()`: Fetches and returns a historical event for the current day.
   - `get_historical_birthdays()`: Fetches and returns a list of notable births on the current day.
   - `get_historical_deaths()`: Fetches and returns a list of notable deaths on the current day.

5. **News Fetching**: Fetches the latest news articles on specified topics from Google News.
   - `fetch_news(topic, num_articles=3)`: Fetches and returns a list of news articles for the given topic.

6. **Fun Fact**: Fetches a random fun fact from the Useless Facts API.
   - `get_fun_fact()`: Fetches and returns a random fun fact.

7. **Counter Management**: Manages a counter stored in a file to keep track of daily emails.
   - `update_counter()`: Updates and returns the current counter value.

8. **File Reading**: Reads the content of a specified file.
   - `read_file(filename)`: Reads and returns the content of a file.

9. **CSS Inlining**: Inlines CSS styles into HTML content for better email compatibility.
   - `inline_css(html, css)`: Inlines the CSS styles into the given HTML content.

Usage:
- Import the required functions from this script.
- Call the functions as needed to fetch data, manage the counter, read files, and inline CSS.

Example:
```
from utils.utils import get_gif, get_quote, get_weather, update_counter, read_file, inline_css

gif_url = get_gif()
quote = get_quote()
weather = get_weather()
counter = update_counter()
html_template = read_file('templates/email_template.html')
css_styles = read_file('static/css/email_style.css')
final_html = inline_css(html_template, css_styles)
```

This example demonstrates how to fetch various data, update the counter, read files, and inline CSS.
"""

import os
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import cssutils
import random
from crossword import Crossword
import openpyxl

# Suppress cssutils logging
cssutils.log.setLevel(logging.CRITICAL)

COUNTER_FILE = 'data_files/counter.txt'

def get_gif():
    logging.info("Fetching GIF of the day.")
    response = requests.get(f"https://api.giphy.com/v1/gifs/random?tag=motivational&api_key={os.getenv('GIPHY_API_KEY')}")
    gif_data = response.json()['data']
    gif_url = gif_data['images']['original']['url']
    logging.info(f"GIF URL: {gif_url}")
    return gif_url

def get_quote():
    logging.info("Fetching quote of the day.")
    response = requests.get("https://api.quotable.io/random?tags=inspirational")
    quote_data = response.json()
    quote = f"{quote_data['content']} - {quote_data['author']}"
    logging.info(f"Quote: {quote}")
    return quote

def get_weather(city, country):
    logging.info(f"Fetching weather forecast for {city}, {country}.")
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={os.getenv('OPENWEATHER_API_KEY')}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        if 'list' not in weather_data or not weather_data['list']:
            logging.error(f"Unexpected API response: {weather_data}")
            return "Weather data unavailable"
        
        # Get today's forecast (first item in the list)
        today_forecast = weather_data['list'][0]
        temp = today_forecast['main']['temp']
        description = today_forecast['weather'][0]['description']
        
        current_temp = today_forecast['main']['temp']
        min_temp = min(item['main']['temp'] for item in weather_data['list'][:8])
        max_temp = max(item['main']['temp'] for item in weather_data['list'][:8])
        description = today_forecast['weather'][0]['description']

        result = f"{current_temp:.1f}Â°C (Min: {min_temp:.1f}Â°C, Max: {max_temp:.1f}Â°C), {description}"
        logging.info(f"Weather fetched successfully: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather: {e}")
        return "Weather data unavailable"
    except KeyError as e:
        logging.error(f"Error parsing weather data: {e}")
        return "Weather data unavailable"
    except Exception as e:
        logging.error(f"Unexpected error in get_weather: {e}")
        return "Weather data unavailable"

def get_weather_icon(description):
    weather_icons = {
        'clear sky': 'â˜€ï¸',
        'few clouds': 'ðŸŒ¤ï¸',
        'scattered clouds': 'â›…',
        'broken clouds': 'â˜ï¸',
        'overcast clouds': 'â˜ï¸',
        'light rain': 'ðŸŒ¦ï¸',
        'moderate rain': 'ðŸŒ§ï¸',
        'heavy intensity rain': 'ðŸŒ§ï¸',
        'very heavy rain': 'ðŸŒ§ï¸',
        'extreme rain': 'ðŸŒ§ï¸',
        'freezing rain': 'ðŸŒ¨ï¸',
        'light intensity shower rain': 'ðŸŒ¦ï¸',
        'shower rain': 'ðŸŒ¦ï¸',
        'heavy intensity shower rain': 'ðŸŒ§ï¸',
        'ragged shower rain': 'ðŸŒ§ï¸',
        'thunderstorm': 'â›ˆï¸',
        'thunderstorm with light rain': 'â›ˆï¸',
        'thunderstorm with rain': 'â›ˆï¸',
        'thunderstorm with heavy rain': 'â›ˆï¸',
        'light thunderstorm': 'ðŸŒ©ï¸',
        'heavy thunderstorm': 'â›ˆï¸',
        'ragged thunderstorm': 'â›ˆï¸',
        'thunderstorm with light drizzle': 'â›ˆï¸',
        'thunderstorm with drizzle': 'â›ˆï¸',
        'thunderstorm with heavy drizzle': 'â›ˆï¸',
        'light intensity drizzle': 'ðŸŒ§ï¸',
        'drizzle': 'ðŸŒ§ï¸',
        'heavy intensity drizzle': 'ðŸŒ§ï¸',
        'light intensity drizzle rain': 'ðŸŒ§ï¸',
        'drizzle rain': 'ðŸŒ§ï¸',
        'heavy intensity drizzle rain': 'ðŸŒ§ï¸',
        'light snow': 'ðŸŒ¨ï¸',
        'snow': 'â„ï¸',
        'heavy snow': 'â„ï¸',
        'sleet': 'ðŸŒ¨ï¸',
        'light shower sleet': 'ðŸŒ¨ï¸',
        'shower sleet': 'ðŸŒ¨ï¸',
        'light rain and snow': 'ðŸŒ¨ï¸',
        'rain and snow': 'ðŸŒ¨ï¸',
        'light shower snow': 'ðŸŒ¨ï¸',
        'shower snow': 'ðŸŒ¨ï¸',
        'heavy shower snow': 'â„ï¸',
        'mist': 'ðŸŒ«ï¸',
        'smoke': 'ðŸŒ«ï¸',
        'haze': 'ðŸŒ«ï¸',
        'sand/dust whirls': 'ðŸŒªï¸',
        'fog': 'ðŸŒ«ï¸',
        'sand': 'ðŸœï¸',
        'dust': 'ðŸŒ«ï¸',
        'volcanic ash': 'ðŸŒ‹',
        'squalls': 'ðŸŒ¬ï¸',
        'tornado': 'ðŸŒªï¸',
    }
    return weather_icons.get(description.lower(), 'ðŸŒ¡ï¸')

def get_weather_tip(description):
    tips = {
        'clear sky': "It's a beautiful day! Consider outdoor activities.",
        'few clouds': "Mild weather ahead. Perfect for a walk!",
        'scattered clouds': "Partly cloudy skies. Don't forget your sunglasses!",
        'broken clouds': "Cloudy with some sun. Dress in layers!",
        'overcast clouds': "Fully cloudy today. Might be a good day for indoor activities.",
        'shower rain': "Light rain expected. Grab an umbrella!",
        'rain': "Rainy day ahead. Stay dry and cozy!",
        'thunderstorm': "Storms brewing. Stay indoors and stay safe!",
        'snow': "Snow day! Bundle up and watch out for icy patches.",
        'mist': "Misty conditions. Drive carefully and use fog lights.",
        'drizzle': "Light drizzle expected. A light jacket should suffice.",
        'light rain': "Light rain on the forecast. Don't forget your umbrella!",
        'moderate rain': "Moderate rain expected. Time for your raincoat!",
        'heavy intensity rain': "Heavy rain ahead. Stay indoors if possible.",
        'freezing rain': "Freezing rain alert! Be extremely cautious if going out."
    }
    return tips.get(description.lower(), "Check the forecast for detailed weather information.")

def get_this_day_in_history():
    logging.info("Fetching this day in history.")
    today = datetime.now()
    month, day = today.month, today.day
    response = requests.get(f"https://history.muffinlabs.com/date/{month}/{day}")
    data = response.json()
    event = data['data']['Events'][0]
    return f"{event['year']}: {event['text']}"

def fetch_news(topic, num_articles=3):
    url = f"https://news.google.com/rss/search?q={topic}&hl=en-CA&gl=CA&ceid=CA:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')[:num_articles]
    
    articles = []
    for item in items:
        article = {
            'title': item.title.text,
            'link': item.link.text,
            'pub_date': item.pubDate.text
        }
        articles.append(article)
    
    return articles

def get_historical_birthdays():
    today = datetime.now()
    month, day = today.month, today.day
    url = f"https://history.muffinlabs.com/date/{month}/{day}"
    response = requests.get(url)
    data = response.json()
    births = data['data']['Births'][:3]
    return [f"{person['year']}: {person['text']}" for person in births]

def get_historical_deaths():
    today = datetime.now()
    month, day = today.month, today.day
    url = f"https://history.muffinlabs.com/date/{month}/{day}"
    response = requests.get(url)
    data = response.json()
    deaths = data['data']['Deaths'][:3]
    return [f"{person['year']}: {person['text']}" for person in deaths]

def get_fun_fact():
    logging.info("Fetching fun fact.")
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    fact_data = response.json()
    return fact_data['text']

def update_counter():
    logging.info("Updating counter.")
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'w') as f:
            f.write('0')
    
    with open(COUNTER_FILE, 'r+') as f:
        counter = int(f.read().strip())
        counter += 1
        f.seek(0)
        f.write(str(counter))
        f.truncate()
    
    logging.info(f"Counter updated to: {counter}")
    return counter

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def inline_css(html, css):
    soup = BeautifulSoup(html, 'html.parser')
    style = cssutils.parseString(css)
    
    for rule in style:
        if rule.type == rule.STYLE_RULE:
            for selector in rule.selectorList:
                for tag in soup.select(selector.selectorText):
                    if not tag.get('style'):
                        tag['style'] = ''
                    tag['style'] += f'{rule.style.cssText};'
    
    style_tag = soup.new_tag('style')
    style_tag.string = css
    soup.head.append(style_tag)
    
    return str(soup)

WORD_BANK = {
  'words': ['python', 'coding', 'template', 'email', 'puzzle', 'clues', 'script', 'function'],
  'clues': {
    'python': {
      'across': 'Programming language used for this project', 
      'down': 'Snake-like name of a programming language'
    },
    'coding': {'down': 'Another term for programming'},
    'template': {'across': 'Used to dynamically generate HTML'},
    'email': {'across': 'This project sends a daily _____'},
    'puzzle': {'down': 'The crosswords is a type of word _____'},
    'clues': {'across': 'Hints to solve the crosswords'},
    'script': {'down': 'A computer program, often written in Python'},
    'function': {'across': 'A reusable block of code that performs a specific task'}      
  }
}

def generate_crosswords() -> dict:
    """Generate a crosswords puzzle with a grid, clues, and answers."""
    words = random.sample(WORD_BANK['words'], 5)
    clues = {direction: [WORD_BANK['clues'][word][direction] for word in words if direction in WORD_BANK['clues'][word]]
             for direction in ['across', 'down']}

    # Create a crossword object
    puzzle = Crossword(13, 13, '-', 5000, words)
    
    # Create an empty grid and populate it with the puzzle
    grid = [['-' for _ in range(puzzle.cols)] for _ in range(puzzle.rows)]

    for i, word in enumerate(words):
        row, col = puzzle.place(word)
        for j, letter in enumerate(word):
            if puzzle.across:
                grid[row][col + j] = letter
            else:
                grid[row + j][col] = letter

    # Assign word numbers based on clues
    grid_numbered = []
    num = 1
    for i, row in enumerate(grid):
        num_row = []
        for j, cell in enumerate(row):
            if cell != '-' and (i == 0 or grid[i-1][j] == '-') and (j == 0 or grid[i][j-1] == '-'):
                num_row.append(num)
                num += 1
            else:
                num_row.append(0)
        grid_numbered.append(num_row)

    return {
        'grid': grid_numbered,
        'across_clues': clues['across'],
        'down_clues': clues['down'],
        'answers': {word: puzzle.solution(word) for word in words}
    }

def get_email_recipients(df):
    """
    Extract email recipients from the keys dataframe.
    Returns a list of tuples (username, email, counter, interests, city, country).
    """
    recipients = df[['Nickname', 'Email', 'Days Receiving the email', 'Interests', 'Current City', 'Current Country']].dropna(subset=['Email'])
    return [
        (row['Nickname'], row['Email'], int(row['Days Receiving the email']) + 1, row['Interests'], row['Current City'], row['Current Country'])
        for _, row in recipients.iterrows()
    ]

def update_recipient_counter(df, email):
    """
    Update the 'Days Receiving the email' counter for the given email.
    """
    df.loc[df['Email'] == email, 'Days Receiving the email'] += 1
    
def get_daily_challenge():
    challenges = [
        "Take a 10-minute walk outside during your break today!",
        "Write down three things you're grateful for this morning.",
        "Try a new healthy recipe for lunch or dinner.",
        "Reach out to a friend or family member you haven't talked to in a while.",
        "Practice mindfulness or meditation for 5 minutes.",
        "Learn a new word in a foreign language and use it in a sentence.",
        "Do a random act of kindness for someone today.",
        "Try a new stretching routine or yoga pose.",
        "Read a chapter from a book you've been meaning to start.",
        "Write down your top three goals for the week and plan how to achieve them.",
        "Try a new hobby or skill for 15 minutes today.",
        "Declutter one small area of your living space.",
        "Listen to a new genre of music during your commute or work.",
        "Take three deep breaths every hour to reduce stress.",
        "Write a short story or poem in 10 minutes.",
        "Start a journal and write your first entry today.",
        "Go for a 15-minute jog or brisk walk.",
        "Try a new fruit or vegetable you've never tasted before.",
        "Compliment three people sincerely today.",
        "Take a digital detox for 2 hours (no phone, computer, TV).",
        "Learn and practice a new joke to share with others.",
        "Do 10 minutes of bodyweight exercises (push-ups, squats, etc.).",
        "Write a thank-you note to someone who has helped you recently.",
        "Try a new productivity technique like the Pomodoro method.",
        "Make a list of 5 things you love about yourself.",
        "Learn the basics of a new language online for 20 minutes.",
        "Create a vision board for your goals and dreams.",
        "Practice active listening in your next conversation.",
        "Try a new type of tea or coffee and savor the experience.",
        "Spend 15 minutes learning about a topic you know nothing about."
    ]
    return random.choice(challenges)
