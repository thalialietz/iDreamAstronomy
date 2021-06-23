from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash)
from model import connect_to_db
# from datetime import date, datetime, timedelta
import datetime
import crud
import model
import os
import requests
import json

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

API_KEY = os.environ['NASA_KEY']
# today = '2021-06-16'
# today = date.today()

today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)
tomorrow = today + datetime.timedelta(days = 1) 


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route('/homepage')
def account_homepage():
    """Show account homepage"""

    username = session.get('username')

    user = crud.get_user_by_username(username)
        
    return render_template('account-homepage.html', user=user)


@app.route("/asteroids")
def all_asteroids():

    asteroids = crud.all_asteroids()
        
    return render_template("all_asteroids.html", asteroids=asteroids)

@app.route('/asteroids/<asteroid_id>')
def get_asteroid_details(asteroid_id):
    """View the details of an asteroid."""

    asteroid = crud.get_asteroid_by_id(asteroid_id)

    return render_template('asteroid-details.html', asteroid=asteroid)

@app.route('/apod')
def show_picture_of_the_day():
    """Show the astronomy picture of the day"""

    date = request.args.get('apod_date')

    url = "https://api.nasa.gov/planetary/apod"
    params = {'date': date, 'thumbs': 'thumbs', 'api_key': API_KEY}
    res = requests.get(url, params)
    apod = res.json()
    
    return render_template('apod.html', apod=apod)

@app.route("/save-favorites")
def save_favorites_asteroid():
    """Save favorite asteroid"""
    user_id = session.get('user_id')
    print(user_id)

    asteroid_id = request.args.get('asteroid_id')
    print(asteroid_id)
    
    favorite_asteroid = crud.create_favorite(user_id, asteroid_id)

    return redirect('/my-journal')

@app.route("/my-journal")
def personal_journal():

    favorites = crud.all_favorites()
    print(favorites)

    return render_template('journal.html', favorites=favorites)


@app.route("/users", methods=['POST'])
def register_user():

    username = request.form.get('username')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if user:
        flash('Cannot create an account with that username and email. Try again')
    else:
        crud.create_user(username, fname, lname, email, password)
        flash('Account created! Please log in')

    return redirect('/')

@app.route('/log-in')
def log_user_in():

    username = request.args.get('user_username')
    password = request.args.get("user_password")

    user = crud.get_user_by_username(username)
    
    if user and user.password == password:
        session['user_id'] = user.user_id
        session['username'] = username
        return redirect('/homepage')
    else:
        flash("Wrong password, try again!")

    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0')
    
