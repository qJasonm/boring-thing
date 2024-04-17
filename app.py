from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
import requests

app = Flask(__name__)

# temperature conversion function
def temp_converter(kelvin_temp):
    return (kelvin_temp - 273.15)*(9/5) + 32

def get_weather_info():
    city = 'denver'
    api_key = '77ccac5efac3aa383ec4263be801fe61'
    weather_info_url = f'https://api.openweathermap.org/data/2.5/weather?q={city},co,us&appid={api_key}'
    return (requests.get(weather_info_url)).json()

def create_data():
    weather_info = get_weather_info()
    data = {
        "city": weather_info['name'],
        "weather": weather_info['weather'][0]['main'],
        "temperature": round(temp_converter(weather_info['main']['temp'])),
        "wind_speed": weather_info['wind']['speed'],
        "visibility": weather_info['visibility']
    }
    return data

data = create_data()

@app.route('/Sloanslake')
def home():
    return render_template('home.html', data=data)

# Scheduler to update data every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=create_data, trigger="interval", seconds=300)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
