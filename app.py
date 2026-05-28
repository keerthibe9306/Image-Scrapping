from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import logging
import pymongo
import json
logging.basicConfig(filename="scrapper.log", level=logging.INFO)
import os

app = Flask(__name__) # initialising the flask app with the name 'app'  

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            query = request.form.get('content', '').strip()
            if not query:
                return 'Please enter a search query.', 400

            save_directory = "images"
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            })

            search_url = f"https://www.bing.com/images/search?q={quote_plus(query)}&form=HDRSC2"
            response = session.get(search_url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            image_items = soup.select('a.iusc')
            results = []
            for item in image_items:
                m_json = item.get('m')
                if not m_json:
                    continue
                try:
                    parsed = json.loads(m_json)
                except json.JSONDecodeError:
                    continue
                image_url = parsed.get('murl') or parsed.get('turl') or parsed.get('imgurl')
                if not image_url:
                    continue
                results.append({'image': image_url})

            img_data = []
            saved_files = []
            for index, item in enumerate(results[:20]):
                image_url = item.get('image')
                if not image_url or not image_url.startswith('http'):
                    continue

                try:
                    image_response = session.get(image_url, timeout=15)
                    image_response.raise_for_status()
                    image_data = image_response.content
                except Exception as exc:
                    logging.info(f"Skipping blocked or invalid image URL: {image_url} - {exc}")
                    continue

                filename = f"{query}_{index}.jpg"
                filepath = os.path.join(save_directory, filename)
                with open(filepath, "wb") as f:
                    f.write(image_data)

                img_data.append({"Index": index, "Image": image_data})
                saved_files.append(filename)

            if not img_data:
                return 'No valid images were found for this query.', 404

            mongo_uri = os.environ.get('MONGODB_URI')
            if mongo_uri and '<password>' not in mongo_uri:
                client = pymongo.MongoClient(mongo_uri)
                db = client['image_scrap']
                review_col = db['image_scrap_data']
                review_col.insert_many(img_data)
            else:
                logging.info('MongoDB URI not configured or contains placeholder; skipping database save.')

            return f"Downloaded {len(saved_files)} images to {save_directory}: {', '.join(saved_files)}"
        except Exception as e:
            logging.exception(e)
            return 'Something went wrong during scraping. Check scrapper.log for details.'
    return render_template('index.html')



    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
