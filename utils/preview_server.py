# utils/preview_server.py

from flask import Flask, render_template, send_from_directory, redirect, url_for
import os

app = Flask(__name__, template_folder='../templates')

# Serve static CSS files
@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.root_path, '../static/css'), filename)

# List all available templates
@app.route('/')
def index():
    template_dir = os.path.join(app.root_path, '../templates')
    templates = [f for f in os.listdir(template_dir) if f.endswith('.html')]
    return render_template('index.html', templates=templates)

# Serve the email templates with example data and CSS
@app.route('/preview/<template>')
def preview(template):
    data = {
        'quote': "Believe you can and you're halfway there.",
        'weather': "Sunny, 25°C",
        'historical_event': "On this day in 1969, Apollo 11 landed on the moon.",
        'news': "Latest news headlines...",
    }
    
    # Read and concatenate all CSS files
    css_files = [
        'static/css/general.css',
        'static/css/container.css',
        'static/css/header.css',
        'static/css/content.css',
        'static/css/weather_widget.css',
        'static/css/sections.css',
        'static/css/gif_container.css',
        'static/css/news_grid.css',
        'static/css/historical_events.css',
        'static/css/footer.css',
    ]
    css_content = ''
    for css_file in css_files:
        with open(css_file, 'r') as f:
            css_content += f.read() + '\n'
    
    # Render the component template within a complete HTML document
    return f'''
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Daily Motivation and Information - {template}</title>
                <style>
                    {css_content}
                </style>
            </head>
            <body>
                <div class="container">
                    {render_template(f'{template}.html', **data)}
                </div>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)