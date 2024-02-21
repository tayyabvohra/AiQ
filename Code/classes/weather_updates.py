import pandas as pd
import requests

def get_weather_updates(location_fictious_address):
    api_key = 'd7cd1f0eb6f54b95ef100b2d83d6b65c'
    weather_data_list = []
    for index, row in location_fictious_address.iterrows():
        lat = row['lat']
        lon = row['lng']
        address = row['Address']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={address}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_data_list.append(weather_data)
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                weather_data_list.append(weather_data)
    return  weather_data_list

def parse_weather_updates(weather_data_list):
    
    parsed_data=[]
    for items in weather_data_list:
        temp_celsius = items.get('main').get('temp') - 273.15
        feels_like_celsius = items.get('main').get('feels_like') - 273.15
        parsed_items = {
            "lon": items.get('coord').get('lon'),
            "lat": items.get('coord').get('lat'),
            "weather_main": items.get('weather')[0].get('main'),
            "weather_description": items.get('weather')[0].get('description'),
            "temp": items.get('main').get('temp'),
            "feels_like": items.get('main').get('feels_like'),
            "pressure": items.get('main').get('pressure'),
            "humidity": items.get('main').get('humidity'),
            "wind_speed": items.get('wind').get('speed'),
            "wind_deg": items.get('wind').get('deg'),
            "clouds": items.get('clouds').get('all'),  
            "temp": temp_celsius,
            "feels_like": feels_like_celsius,
        }
        parsed_data.append(parsed_items)
    return  parsed_data