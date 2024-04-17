from flask import Flask, render_template
import requests 

def temp_converter(kelvin_temp):
    return (kelvin_temp - 273.15)*(9/5)+32

city = 'denver'
api_key = '77ccac5efac3aa383ec4263be801fe61'
weather_info_url = f'https://api.openweathermap.org/data/2.5/weather?q={city},co,us&appid={api_key}'
weather_info = (requests.get(weather_info_url)).json()

app = Flask(__name__)

@app.route('/')
def home():
    data = get_data(weather_info)
    return render_template('home.html', data=data)

def get_data(data):
    data = {
        "city": data['name'],
        "weather": data['weather'][0]['main'],
        "temperature": round(temp_converter(data['main']['temp'])),
        "wind_speed": data['wind']['speed'],
        "visibility": data['visibility']
    }
    return data

if __name__ == "__main__":
    app.run(debug=True)