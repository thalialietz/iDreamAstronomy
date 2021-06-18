"""CRUD operations."""

from model import db, User, Favorite, Asteroid, connect_to_db
import json
import os
import requests

API_KEY = os.environ['NASA_KEY']

def create_user(username, fname, lname, email, password):
    """Create and return a new user."""

    user = User(username=username, fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_asteroid(api_asteroid_id, name, potentially_hazardous, close_approach_date, nasa_jpl_url, relative_velocity_kilometers_per_hour, relative_velocity_miles_per_hour, 
orbiting_body, miss_distance_kilometers, miss_distance_miles, estimated_diameter_kilometers_min,
estimated_diameter_kilometers_max, estimated_diameter_miles_min, estimated_diameter_miles_max):

    asteroid = Asteroid(api_asteroid_id=api_asteroid_id, name=name, potentially_hazardous=potentially_hazardous, close_approach_date=close_approach_date, nasa_jpl_url=nasa_jpl_url, 
    relative_velocity_kilometers_per_hour=relative_velocity_kilometers_per_hour, relative_velocity_miles_per_hour=relative_velocity_miles_per_hour, 
    orbiting_body=orbiting_body, miss_distance_kilometers=miss_distance_kilometers, miss_distance_miles=miss_distance_miles, 
    estimated_diameter_kilometers_min=estimated_diameter_kilometers_min, estimated_diameter_kilometers_max=estimated_diameter_kilometers_max,
    estimated_diameter_miles_min=estimated_diameter_miles_min, estimated_diameter_miles_max=estimated_diameter_miles_max)

    db.session.add(asteroid)
    db.session.commit()

    return asteroid

def all_asteroids():

    return Asteroid.query.all()

def get_asteroid_by_id(api_asteroid_id):

    return Asteroid.query.filter_by(api_asteroid_id=api_asteroid_id).one()

def get_picture_of_the_day():

    url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    # params = {'API_KEY': API_KEY}
    res = requests.get(url)
    data = res.json()

def all_users():

    return User.query.all()

def get_user_by_id(user_id):

    return User.query.get(user_id)

def get_user_by_username(username):

    return User.query.filter(User.username == username).first()

    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)