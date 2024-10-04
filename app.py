from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import uuid
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

WEATHER_API_KEY = "62b83a7f9212447aba853454240907"
MAPS_API_KEY = "AIzaSyA6JxoN5m0SE7zMcZpk1FtYhEpX3r4lW9Q"
WEATHER_URL = "http://api.weatherapi.com/v1/forecast.json"


todos = []

@app.route('/')
def index():
    now = datetime.now()
    for todo in todos:
        if todo['due_date'] < now and not todo['overdue']:
            todo['overdue'] = True
            flash(f"タスク '{todo['title']}' の期限が過ぎています！")

    weather_params = {
        'key': WEATHER_API_KEY,
        'q': 'Takamatsu',
        'days': 1,
        'aqi': 'no',
        'alerts': 'no'
    }
    response = requests.get(WEATHER_URL, params=weather_params)
    weather_data = response.json() if response.status_code == 200 else None
    forecast_date = weather_data['forecast']['forecastday'][0]['date'] if weather_data else None

    return render_template(
        'index.html', 
        todos=todos, 
        weather_data=weather_data, 
        maps_api_key=MAPS_API_KEY,
        forecast_date=forecast_date  
    )

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')
    new_todo = {
        'id': uuid.uuid4().hex,
        'title': title,
        'due_date': due_date,
        'overdue': False
    }
    todos.append(new_todo)
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    global todos
    todos = [todo for todo in todos if todo['id'] != id]
    return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update(id):
    title = request.form['title']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')
    for todo in todos:
        if todo['id'] == id:
            todo['title'] = title
            todo['due_date'] = due_date
            todo['overdue'] = False
            break
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()
    if query:
        filtered_todos = [todo for todo in todos if query in todo['title'].lower()]
    else:
        filtered_todos = todos

    now = datetime.now()
    for todo in filtered_todos:
        if todo['due_date'] < now and not todo['overdue']:
            todo['overdue'] = True
            flash(f"タスク '{todo['title']}' の期限が過ぎています！")

    weather_params = {
        'key': WEATHER_API_KEY,
        'q': 'Takamatsu',
        'days': 1,
        'aqi': 'no',
        'alerts': 'no'
    }
    response = requests.get(WEATHER_URL, params=weather_params)
    weather_data = response.json() if response.status_code == 200 else None
    forecast_date = weather_data['forecast']['forecastday'][0]['date'] if weather_data else None

    return render_template(
        'index.html', 
        todos=filtered_todos, 
        weather_data=weather_data, 
        maps_api_key=MAPS_API_KEY,
        forecast_date=forecast_date  
    )

if __name__ == '__main__':
    app.run(debug=True)
