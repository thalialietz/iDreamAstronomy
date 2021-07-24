"""CRUD operations."""

from model import db, User, Favorite, Asteroid, connect_to_db


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


def create_favorite(user_id, asteroid_id):
    
    favorite = Favorite(user_id=user_id, asteroid_id=asteroid_id)

    db.session.add(favorite)
    db.session.commit()

    return favorite


def all_favorites():

    return Favorite.query.all()


def get_favorite_by_user_id(user_id):

    return Favorite.query.filter(Favorite.user_id == user_id).all()


def all_asteroids():

    return Asteroid.query.all()


def get_asteroid_by_api_id(api_asteroid_id):

    return Asteroid.query.filter(Asteroid.api_asteroid_id == api_asteroid_id).first()
    
    
def all_users():

    return User.query.all()


def get_user_by_id(user_id):

    return User.query.get(user_id)
    

def get_user_by_username(username):

    return User.query.filter(User.username == username).first()


def get_user_by_email(email):

    return User.query.filter(User.email == email).first()

    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)