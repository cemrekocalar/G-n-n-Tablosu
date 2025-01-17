from flask import Flask, render_template, jsonify
import requests
import random
import datetime

app = Flask(__name__)

""" Tablo verilerini çekme """
BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

def get_painting_ids():
    
    response = requests.get(f"{BASE_URL}/search?q=painting&hasImages=true")
    if response.status_code == 200:
        data = response.json()
        return data.get('objectIDs', [])
    return []

def get_painting_details(object_id):
    
    response = requests.get(f"{BASE_URL}/objects/{object_id}")
    if response.status_code == 200:
        return response.json()
    return {}

def get_daily_painting():
    """Günün tablosu seçimi yapıyoruz"""
    painting_ids = get_painting_ids()
    if painting_ids:
        today = datetime.date.today()
        random.seed(today.toordinal())  # Her gün aynı tabloyu seçmek için
        selected_id = random.choice(painting_ids)
        return get_painting_details(selected_id)
    return {}

@app.route('/')
def index():
    """Ana sayfada Günün tablosunu gösterir."""
    daily_painting = get_daily_painting()
    if daily_painting:
        return render_template('index.html', painting=daily_painting)
    else:
        return "<h1>Bugün için bir tablo bulunamadı.</h1>", 404

@app.route('/api/daily-painting')
def api_daily_painting():
    
    daily_painting = get_daily_painting()
    return jsonify(daily_painting)

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__, static_folder='static')
