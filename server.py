from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash)
from model import connect_to_db
import crud
import model
import os
import requests
import json

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

API_KEY = os.environ['NASA_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route("/asteroids")
def all_asteroids():

    asteroids = crud.all_asteroids()
        
    return render_template("all_asteroids.html", asteroids=asteroids)

@app.route('/asteroids/<api_asteroid_id>')
def get_asteroid_details(api_asteroid_id):
    """View the details of an asteroid."""

    asteroid = crud.get_asteroid_by_id(api_asteroid_id)

    return render_template('asteroid-details.html', asteroid=asteroid)

@app.route("/users", methods=['POST'])
def register_user():

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if user:
        flash('Cannot create an account with that username and email. Try again')
    else:
        crud.create_user(username, email, password)
        flash('Account created! Please log in')

    return redirect('/')

@app.route('/log-in', methods=["POST"])
def log_user_in():

    username = request.form.get('user_username')
    password = request.form.get("user_password")

    user = crud.get_user_by_username(username)

    if user and user.password == password:
        flash("Logged in!")
        session['username'] = username
    else:
        flash("Wrong password, try again!")

    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0')
    
