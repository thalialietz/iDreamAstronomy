"""CRUD operations."""

from model import db, User, Favorite, Asteroid, connect_to_db
from sqlalchemy import or_


def create_user(username, fname, lname, email, password):
    """Create and return a new user."""

    user = User(username=username, fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def create_asteroid(api_asteroid_id, name, potentially_hazardous, close_approach_date, nasa_jpl_url, relative_velocity_kilometers_per_hour, relative_velocity_miles_per_hour, 
orbiting_body, miss_distance_kilometers, miss_distance_miles, estimated_diameter_kilometers_min,
estimated_diameter_kilometers_max, estimated_diameter_miles_min, estimated_diameter_miles_max):
    """Create and return a new asteroid"""

    asteroid = Asteroid(api_asteroid_id=api_asteroid_id, name=name, potentially_hazardous=potentially_hazardous, close_approach_date=close_approach_date, nasa_jpl_url=nasa_jpl_url, 
    relative_velocity_kilometers_per_hour=relative_velocity_kilometers_per_hour, relative_velocity_miles_per_hour=relative_velocity_miles_per_hour, 
    orbiting_body=orbiting_body, miss_distance_kilometers=miss_distance_kilometers, miss_distance_miles=miss_distance_miles, 
    estimated_diameter_kilometers_min=estimated_diameter_kilometers_min, estimated_diameter_kilometers_max=estimated_diameter_kilometers_max,
    estimated_diameter_miles_min=estimated_diameter_miles_min, estimated_diameter_miles_max=estimated_diameter_miles_max)

    db.session.add(asteroid)
    db.session.commit()

    return asteroid


def create_favorite(user_id, asteroid_id):
    """Create and return a new favorite"""
    
    favorite = Favorite(user_id=user_id, asteroid_id=asteroid_id)

    db.session.add(favorite)
    db.session.commit()

    return favorite


def all_favorites():
    """Returns all favorites from the database"""

    return Favorite.query.all()


def get_favorite_by_user_id(user_id):
    """Returns a favorite by the user id"""

    return Favorite.query.filter(Favorite.user_id == user_id).all()


def all_asteroids():
    """Returns all asteroids from the database"""

    return Asteroid.query.all()


def get_asteroid_by_api_id(api_asteroid_id):
    """Returns an asteroid by the api id"""

    return Asteroid.query.filter(Asteroid.api_asteroid_id == api_asteroid_id).first()
    
    
def all_users():
    """Returns all user in the current database"""

    return User.query.all()


def get_user_by_id(user_id):
    """Returns a user by the user id"""

    return User.query.get(user_id)
    

def get_user_by_username(username):
    """Returns a user by the username"""

    return User.query.filter(User.username == username).first()


def get_user_by_email(email):
    """Returns a user by the user email"""

    return User.query.filter(User.email == email).first()

def get_user_by_email_or_username(user_info):
    """Returns a user by the user email or username"""

    return User.query.filter(or_(User.email == user_info, User.username == user_info)).first()


def delete_asteroid_by_user_id(user_id, asteroid_id):

    favorite = Favorite.query.filter(Favorite.user_id == user_id, Favorite.asteroid_id == asteroid_id).first()
    db.session.delete(favorite)
    db.session.commit()

    return None



        
if __name__ == '__main__':
    from server import app
    connect_to_db(app)