"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} username={self.username}>'

class Favorite(db.Model):
    """Favorites Asteroids"""

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    asteroid_id = db.Column(db.Integer, db.ForeignKey('asteroids.asteroid_id'))


    def __repr__(self):
        return f'<Favorite favorite_id={self.favorite_id} user_id={self.user_id} asteroid_id={self.asteroid_id}>'

class Asteroid(db.Model):
    """All Asteroids information from API"""

    __tablename__ = 'asteroids'

    asteroid_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String)
    potentially_hazardous = db.Column(db.Boolean) #values can be T or F or/and 1 or 0
    close_approach_date = db.Column(db.DateTime)
    nasa_jpl_url = db.Column(db.String)
    relative_velocity_kilometers_per_hour = db.Column(db.Integer)
    relative_velocity_miles_per_hour = db.Column(db.Integer)
    orbiting_body = db.Column(db.String)
    miss_distance_kilometers = db.Column(db.Integer)
    miss_distance_miles = db.Column(db.Integer)
    estimated_diameter_kilometers_min = db.Column(db.Integer)
    estimated_diameter_kilometers_max = db.Column(db.Integer)
    estimated_diameter_miles_min = db.Column(db.Integer)
    estimated_diameter_miles_max = db.Column(db.Integer)

    def __repr__(self):
        return f'<Asteroid asteroid_id={self.asteroid_id} name={self.name} nasa_jpl_url={self.nasa_jpl_url}>'                   


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)