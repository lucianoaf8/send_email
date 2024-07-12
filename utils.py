import json
import random
import logging
from PIL import Image
import io
import base64
import requests

class APIError(Exception):
    """Custom exception for API failures"""
    pass

def handle_api_error(api_name, error):
    logging.error(f"Error in {api_name} API: {str(error)}")
    raise APIError(f"{api_name} API failed: {str(error)}")

def compress_image(image_url, quality=85):
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=quality, optimize=True)
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode()

def ab_test(option_a, option_b):
    return random.choice([option_a, option_b])

def get_fallback_data(api_name):
    with open('fallback_data.json', 'r') as f:
        fallback_data = json.load(f)
    return fallback_data.get(api_name, "Fallback data not available")

def update_fallback_data(api_name, data):
    with open('fallback_data.json', 'r+') as f:
        fallback_data = json.load(f)
        fallback_data[api_name] = data
        f.seek(0)
        json.dump(fallback_data, f, indent=2)
        f.truncate()