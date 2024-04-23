from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template,jsonify
import requests
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
import numpy as np

app = Flask(__name__)

#===========================================================

def create_model():
    num_input_variables = 5

    model = Sequential([
        Dense(20, input_dim=num_input_variables, activation='relu'),
        Dense(16, activation='relu'),
        Dense(8, activation='relu'),
        Dense(8, activation='relu'),
        Dense(5, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

model = create_model()
model.load_weights('team_project\model_weights99.h5')

#===========================================================

def temp_converter(kelvin_temp):
    return (kelvin_temp - 273.15) * (9/5) + 32

def get_weather_info(city):
    api_key = '77ccac5efac3aa383ec4263be801fe61'
    weather_info_url = f'https://api.openweathermap.org/data/2.5/weather?q={city},co,us&appid={api_key}'
    return requests.get(weather_info_url).json()

def create_data(city):
    weather_info = get_weather_info(city)
    data = {
        "city": weather_info['name'],
        "weather": weather_info['weather'][0]['main'],
        "temperature": round(temp_converter(weather_info['main']['temp'])),
        "min_temp": round(temp_converter(weather_info['main']['temp_min'])),
        "max_temp": round(temp_converter(weather_info['main']['temp_max'])),
        "wind_speed": weather_info['wind']['speed'],
        "visibility": weather_info['visibility']
    }
    return data

def predict_data(data):
    X = np.array([data['temperature'],data['min_temp'],data['max_temp'],data['visibility'],data['wind_speed']])
    X = X.reshape(1, -1)
    prediction = model.predict(X)[0][0]
    binary_prediction = (prediction > 0.5).astype(int)
    advice = {"advice" :"Good for outdoor activities" if binary_prediction < 0.5 else "Not advisable for outdoor activities"}
    return advice

def update_and_predict(city):
    data = create_data(city)
    result = predict_data(data)

@app.route('/Sloanslake')
def sloanslake():
    city = 'wheat ridge'
    data = create_data(city)
    result = predict_data(data)
    return render_template('Sloanslake.html', data=data, result = result)

@app.route('/Sloanslake/json', methods=['GET'])
def sloanslake_json():
    city = 'wheat ridge'
    data = create_data(city)
    result = predict_data(data)
    data['prediction'] = result
    return jsonify(data)

@app.route('/CherryCreek')
def cherrycreek():
    city = 'denver'
    data = create_data(city)
    result = predict_data(data)
    return render_template('CherryCreek.html', data=data, result = result)

@app.route('/CherryCreek/json', methods=['GET'])
def cherrycreek_json():
    city = 'denver'
    data = create_data(city)
    result = predict_data(data)
    data['prediction'] = result
    return jsonify(data)

@app.route("/Lairo'thebear")
def Lairothebear():
    city = 'idledale'
    data = create_data(city)
    result = predict_data(data)
    return render_template('Lairothebear.html', data=data, result = result)

@app.route("/Lairo'thebear/json", methods=['GET'])
def Lairothebear_json():
    city = 'idledale'
    data = create_data(city)
    result = predict_data(data)
    data['prediction'] = result
    return jsonify(data)

# # Scheduler to update data every 5 minutes
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=create_data, args=('edge water',), trigger="interval", seconds=300)
# scheduler.add_job(func=create_data, args=('denver',), trigger="interval", seconds=300)
# scheduler.add_job(func=create_data, args=('idledale',), trigger="interval", seconds=300)
# scheduler.start()

scheduler = BackgroundScheduler()
cities = ['edge water', 'denver', 'idledale']
for city in cities:
    scheduler.add_job(func=update_and_predict, args=(city,), trigger="interval", minutes=5)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
