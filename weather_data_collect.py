import csv
import time
import os
import requests
import time
import datetime

api_key = '77ccac5efac3aa383ec4263be801fe61'
cities = ['Denver','Golden','Boulder','Greeley','Colorado Springs','Pueblo','Fort Collins']
def write_to_csv(data,current_time):
    # Check if the file is empty
    
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        file_empty = os.stat('data.csv').st_size == 0
        if file_empty:
            writer.writerow([
                'City Name',
                'Weather Main',
                'Temperature',
                'Min Temperature',
                'Max Temperature',
                'Humidity',
                'Visibility',
                'Wind Speed',
                'Wind Degree',
                'Wind Gust',
                'Sunrise',
                'Sunset',
                'Time'
            ])
        
        writer.writerow([
            data['name'],
            data['weather'][0]['main'],
            data['main']['temp'],
            data['main']['temp_min'],
            data['main']['temp_max'],
            data['main']['humidity'],
            data['visibility'],
            data['wind']['speed'],
            data['wind']['deg'],
            data['wind']['gust'],
            data['sys']['sunrise'],
            data['sys']['sunset'],
            current_time
        ])

def temp_converter(kelvin_temp):
    return (kelvin_temp - 273.15)*(9/5)+32

for city in cities:
    current_datetime = datetime.datetime.now()
    weather_info_url = f'https://api.openweathermap.org/data/2.5/weather?q={city},co,us&appid={api_key}'
    weather_info = (requests.get(weather_info_url)).json()

    write_to_csv(weather_info,current_datetime)

time.sleep(1800)

