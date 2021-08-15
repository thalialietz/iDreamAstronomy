"""Script to seed database."""

import os
import json
import requests
from flask import request
from random import choice, randint
from datetime import datetime

import crud
import model
import server

API_KEY = os.environ['NASA_KEY']
model.connect_to_db(server.app)
model.db.create_all()
os.system('dropdb asteroidsdb')
os.system('createdb asteroidsdb')  
#not seeding asteroids, just only adding them when users favorite them.
