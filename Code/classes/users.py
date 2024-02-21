import pandas as pd
import requests


def get_users_data():
    json_url = 'https://jsonplaceholder.typicode.com/users'
    response = requests.get(json_url)
    if response.status_code == 200:
        json_data=response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
    return json_data

def parse_users_data(json_data):
    parsed_data = []

    for item in json_data:
        parsed_item = {
            "customer_id": item.get("id"),
            "name": item.get("name"),
            "username": item.get("username"),
            "city": item.get("address").get("city"),
            "lat": item.get("address").get("geo").get("lat"),
            "lng": item.get("address").get("geo").get("lng"),
        }
        parsed_data.append(parsed_item)
    return parsed_data