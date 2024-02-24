import pandas as pd
import requests
import pyodbc
from sqlalchemy import create_engine
from classes.users import get_users_data,parse_users_data
from classes.locations import get_fictious_locations
from classes.weather_updates import get_weather_updates,parse_weather_updates
from classes.push_db import push_df_to_db
import os

def main():
    current_path = os.getcwd()
    users=get_users_data()
    users_parsed_dict=parse_users_data(users)
    users_df = pd.DataFrame(users_parsed_dict)
    file_path = f"csv\AiQ.csv"
    # file_path = f"{current_path}/csv/AiQ.csv" 
    orders_details = pd.read_csv(file_path)
   

    current_path = os.getcwd()
    print("Current Path:", current_path)

    merged_data = pd.merge(orders_details, users_df, on='customer_id', how='left')
    merged_data['lng']=merged_data['lng'].astype(float)
    merged_data['lat']=merged_data['lat'].astype(float)

    locations_df=get_fictious_locations()
    location_fictious_address = pd.merge(locations_df, merged_data, on='city', how='left')
    location_fictious_address = location_fictious_address[['city', 'Address', 'lat', 'lng']]
    location_fictious_address = location_fictious_address.drop_duplicates()

    get_weather_data=get_weather_updates(location_fictious_address)
    parse_weather_data=parse_weather_updates(get_weather_data)
    weathers_df = pd.DataFrame(parse_weather_data)

    weathers_df['lon']=weathers_df['lon'].astype(float)
    weathers_df['lat']=weathers_df['lat'].astype(float)

    users_df['lng']=users_df['lng'].astype(float)
    users_df['lat']=users_df['lat'].astype(float)

    weather_df=pd.merge(weathers_df,users_df,left_on=['lon','lat'],right_on=['lng','lat'],how='left')
    weather_df=weather_df[['lon','lat','city','weather_main','weather_description','temp']]

    total_sales_dataset = pd.merge(merged_data, weather_df, left_on=['lng','lat'], right_on=['lon','lat'], how='left')
    total_sales_dataset = total_sales_dataset.drop(columns=['lon'])

    push_df_to_db(total_sales_dataset,'total_sales_dataset')
    push_df_to_db(users_df,'users_details')
    push_df_to_db(location_fictious_address,'location_fictious_address')
    push_df_to_db(weather_df,'weather_details')
    push_df_to_db(orders_details,'orders_details')



if __name__ == "__main__":
    main()