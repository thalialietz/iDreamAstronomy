"""Script to seed database."""

import os
import json
import requests
from random import choice, randint
from datetime import datetime

import crud
import model
import server

API_KEY = os.environ['NASA_KEY']

os.system('dropdb asteroids')
os.system('createdb asteroids')
model.connect_to_db(server.app)
model.db.create_all()


asteroids = {}
def get_all_asteroids():

    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {'start_date': '2021-06-01', 
      'end_date': '2021-06-02', 
      'API_KEY': API_KEY
    }
    res = requests.get(url, params=params)
    neo_data = res.json()
    
    for date in neo_data['near_earth_objects']:
        for asteroid in neo_data['near_earth_objects'][date]:
            api_asteroid_id = asteroid['neo_reference_id']
            name = asteroid['name']
            potentially_hazardous = asteroid['is_potentially_hazardous_asteroid']
            close_approach_date = asteroid['close_approach_data'][0]['close_approach_date_full']
            nasa_jpl_url = asteroid['nasa_jpl_url']
            relative_velocity_kilometers_per_hour = asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
            relative_velocity_miles_per_hour = asteroid['close_approach_data'][0]['relative_velocity']['miles_per_hour']
            orbiting_body = asteroid['close_approach_data'][0]['orbiting_body']
            miss_distance_kilometers = asteroid['close_approach_data'][0]['miss_distance']['kilometers']
            miss_distance_miles = asteroid['close_approach_data'][0]['miss_distance']['miles']
            estimated_diameter_kilometers_min = asteroid['estimated_diameter']['kilometers']['estimated_diameter_min']
            estimated_diameter_kilometers_max = asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']
            estimated_diameter_miles_min = asteroid['estimated_diameter']['miles']['estimated_diameter_min']
            estimated_diameter_miles_max = asteroid['estimated_diameter']['miles']['estimated_diameter_max']

            # asteroids[name] = asteroid_id, potentially_hazardous, close_approach_date, nasa_jpl_url, relative_velocity_kilometers_per_hour, relative_velocity_miles_per_hour, orbiting_body, miss_distance_kilometers, miss_distance_miles, estimated_diameter_kilometers_min, estimated_diameter_kilometers_max, estimated_diameter_miles_min, estimated_diameter_miles_max
            asteroids = crud.create_asteroid(api_asteroid_id, name, potentially_hazardous, close_approach_date, nasa_jpl_url, relative_velocity_kilometers_per_hour, relative_velocity_miles_per_hour, 
orbiting_body, miss_distance_kilometers, miss_distance_miles, estimated_diameter_kilometers_min,
estimated_diameter_kilometers_max, estimated_diameter_miles_min, estimated_diameter_miles_max)
            # asteroid_list.append((name, close_approach_date, miss_distance_kilometers, estimated_diameter_kilometers_min, nasa_jpl_url))

get_all_asteroids()


