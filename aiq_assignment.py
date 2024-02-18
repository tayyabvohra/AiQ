import pandas as pd
import requests
import pyodbc
from sqlalchemy import create_engine

json_url = 'https://jsonplaceholder.typicode.com/users'
response = requests.get(json_url)
if response.status_code == 200:
    json_data=response.json()
else:
    print(f"Request failed with status code {response.status_code}")

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
    
users_df = pd.DataFrame(parsed_data)

orders_details=pd.read_csv('AiQ.csv')

merged_data = pd.merge(orders_details, users_df, on='customer_id', how='left')

merged_data['lng']=merged_data['lng'].astype(float)
merged_data['lat']=merged_data['lat'].astype(float)

import pandas as pd

# Create a dictionary with locations and addresses
locations_dict = {
    "city": ["Roscoeview", "Aliyaview", "Bartholomebury", "McKenziehaven", "Lebsackbury",
                 "Howemouth", "South Elvis", "Gwenborough", "Wisokyburgh", "South Christy"],
    "Address": ["Roscoe Village, Chicago, IL, USA",
                "303, Al-Falah Building, Shahrah-e-Quaid-e-Azam, Garhi Shahu, Lahore, Punjab 54000, Pakistan",
                "Null",  # Address not found
                "11 Hillcross St # 83, McKenzie, AL 36456, USA",
                "Null",  # Address not found
                "Null",  # Address not found
                "Memphis, TN 38106, USA",
                "Guisborough TS14, UK",
                "Winchburgh, UK",
                "2490 S Woodworth Loop Suite 301, Palmer, AK 99645, USA"]
}

df = pd.DataFrame(locations_dict)
location_fictious_address = pd.merge(df, merged_data, on='city', how='left')
location_fictious_address = location_fictious_address[['city', 'Address', 'lat', 'lng']]
location_fictious_address = location_fictious_address.drop_duplicates()

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

weather_df = pd.DataFrame(parsed_data)


# weather_df['lon']=weather_df['lon'].astype(float)
# weather_df['lat']=weather_df['lat'].astype(float)
# users_df['lng']=users_df['lng'].astype(float)
# users_df['lat']=users_df['lat'].astype(float)
weather_df=pd.merge(weather_df,users_df,left_on=['lon','lat'],right_on=['lng','lat'],how='left')
# weather_df=weather_df[['lon','lat','city','weather_main','weather_description','temp']]


weather_df=weather_df[['lon','lat','city','weather_main','weather_description','temp']]

total_sales_dataset = pd.merge(merged_data, weather_df, left_on=['lng','lat'], right_on=['lon','lat'], how='left')

total_sales_dataset = total_sales_dataset.drop(columns=['lon'])

# Replace the placeholders with your actual SQL Server connection details
def push_df_to_db(df,table_name):
    host = 'DESKTOP-6P1LUS8'
    database_name = 'AiQ'
    driver = 'SQL Server Native Client 11.0'
    connection_string = f"mssql+pyodbc://{host}/{database_name}?driver={driver}"
    engine = create_engine(connection_string)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    engine.dispose()


push_df_to_db(total_sales_dataset,'total_sales_dataset')
push_df_to_db(users_df,'users_details')
push_df_to_db(location_fictious_address,'location_fictious_address')
push_df_to_db(weather_df,'weather_details')
push_df_to_db(orders_details,'orders_details')



