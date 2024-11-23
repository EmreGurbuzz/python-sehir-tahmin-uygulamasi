from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from views import main
from geopy.distance import geodesic
import random
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.register_blueprint(main)

MAX_ATTEMPTS = 5
MAX_HINTS = 2

# Load city data from JSON file
with open('static/cities.json', 'r') as f:
    city_data = json.load(f)['cities']

@app.before_request
def before_request():
    if 'attempts' not in session:
        session['attempts'] = 0
    if 'guesses' not in session:
        session['guesses'] = []
    if 'hints' not in session:
        session['hints'] = []
    if 'hint_count' not in session:
        session['hint_count'] = MAX_HINTS
    if 'city' not in session:
        generate_new_city()
    if 'score' not in session:
        session['score'] = 0
    if 'hint_index' not in session:
        session['hint_index'] = 0

def generate_new_city():
    try:
        city = random.choice(city_data)
        session['city'] = city['name']
        session['city_coordinates'] = tuple(city['coordinates'])
        session['hints'] = city['hints']  # Use all hints from the city data
        session['famous_foods'] = city['famous_foods']
        session['famous_places'] = city['famous_places']
        session['guesses'] = []  # Reset guesses
        session['hint_count'] = MAX_HINTS  # Reset hint count
        session['hint_index'] = 0  # Reset hint index
    except Exception as e:
        print(f"Yeni şehir oluşturulurken hata: {e}")
        session['city'] = None
        session['city_coordinates'] = (0, 0)
        session['hints'] = []
        session['famous_foods'] = []
        session['famous_places'] = []
        session['guesses'] = []
        session['hint_count'] = MAX_HINTS
        session['hint_index'] = 0

@app.route('/')
def index():
    return render_template('index.html', cities=city_data)

@app.route('/guess', methods=['POST'])
def guess():
    if session['attempts'] >= MAX_ATTEMPTS:
        flash(f'Tahmin hakkınız doldu! Doğru cevap: {session["city"]}', 'danger')
        return redirect(url_for('main.index'))

    user_city = request.form['city']
    user_coordinates = get_city_coordinates(user_city)
    
    if check_city_guess(user_city, session['city']):
        flash('Doğru tahmin ettiniz! Yeni soruya geçtiniz.', 'success')
        session['guesses'].append({'city': user_city, 'distance': 0})
        session['score'] += 1  # Increase score on correct guess
        print(f"Tahmin edilen şehir: {user_city}")
        generate_new_city()
    else:
        distance = geodesic(session['city_coordinates'], user_coordinates).km
        flash(f'Yanlış tahmin! Tahmin ettiğiniz şehir: {user_city}, Mesafe: {distance:.2f} km.', 'danger')
        session['guesses'].append({'city': user_city, 'distance': distance})
        session['attempts'] += 1
        if session['attempts'] >= MAX_ATTEMPTS:
            flash(f'Tahmin hakkınız doldu! Doğru cevap: {session["city"]}', 'danger')
    
    return redirect(url_for('main.index'))

def check_city_guess(user_city, correct_city):
    return user_city.lower() == correct_city.lower()

@app.route('/hint', methods=['GET'])
def hint():
    if session['hint_count'] > 0:
        session['hint_count'] -= 1
        hint_index = session['hint_index']
        if hint_index % 2 == 0:
            hint = session['famous_foods'][hint_index // 2]
        else:
            hint = session['famous_places'][hint_index // 2]
        session['hint_index'] += 1
        return jsonify({'hint': hint})
    else:
        return jsonify({'error': 'İpucu hakkınız kalmadı!'})

def get_city_coordinates(city_name):
    for city in city_data:
        if city['name'].lower() == city_name.lower():
            return tuple(city['coordinates'])
    return (0, 0)

@app.route('/reset')
def reset():
    session.pop('attempts', None)
    session.pop('guesses', None)
    session.pop('hints', None)
    session.pop('city', None)
    session.pop('city_coordinates', None)
    session.pop('score', None)
    session.pop('hint_index', None)
    return redirect(url_for('main.index'))

if __name__ == '__main__':
    app.run(debug=True)