from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template,jsonify
import requests

app = Flask(__name__)

# temperature conversion function
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

@app.route('/Sloanslake')
def sloanslake():
    city = 'wheat ridge'
    data = create_data(city)
    return render_template('Sloanslake.html', data=data)

@app.route('/Sloanslake/json', methods=['GET'])
def sloanslake_json():
    city = 'wheat ridge'
    data = create_data(city)  # Assuming create_data function is defined elsewhere
    return jsonify(data)

@app.route('/CherryCreek')
def cherrycreek():
    city = 'denver'
    data = create_data(city)
    return render_template('CherryCreek.html', data=data)

@app.route('/CherryCreek/json', methods=['GET'])
def cherrycreek_json():
    city = 'denver'
    data = create_data(city)  # Assuming create_data function is defined elsewhere
    return jsonify(data)

@app.route("/Lairo'thebear")
def Lairothebear():
    city = 'idledale'
    data = create_data(city)
    return render_template('Lairothebear.html', data=data)

@app.route("/Lairo'thebear/json", methods=['GET'])
def Lairothebear_json():
    city = 'idledale'
    data = create_data(city)  # Assuming create_data function is defined elsewhere
    return jsonify(data)

# Scheduler to update data every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=create_data, args=('edge water',), trigger="interval", seconds=300)
scheduler.add_job(func=create_data, args=('denver',), trigger="interval", seconds=300)
scheduler.add_job(func=create_data, args=('idledale',), trigger="interval", seconds=300)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
