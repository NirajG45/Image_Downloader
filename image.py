from flask import Flask, render_template, request, redirect, url_for
import os
import requests
from urllib.parse import urlparse

app = Flask(__name__)
DOWNLOAD_FOLDER = 'static/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    downloaded_file = None

    if request.method == 'POST':
        image_url = request.form.get('image_url')
        if image_url:
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    # Extract image file name
                    parsed_url = urlparse(image_url)
                    filename = os.path.basename(parsed_url.path)
                    file_path = os.path.join(DOWNLOAD_FOLDER, filename)

                    # Save image to server
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    downloaded_file = filename
            except Exception as e:
                print(f"Error downloading image: {e}")
    
    return render_template('index.html', file=downloaded_file)

if __name__ == '__main__':
    app.run(debug=True)
