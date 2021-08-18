from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash)
from threading import Thread
from model import db, User, connect_to_db
import crud
import os
import requests
import json
from flask_mail import Message, Mail
import jwt
from datetime import datetime, timedelta
from sqlalchemy import exc
import random


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
app.config['SECRET_KEY'] = str('flasksecretkey')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_ADDRESS']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
mail = Mail(app)

API_KEY = os.environ['NASA_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    if 'username' in session:
        return redirect("/profile")
    else:
        return render_template('homepage.html')


@app.route('/profile')
def account_homepage():
    """Show account homepage"""

    username = session.get('username')

    user = crud.get_user_by_username(username)

    return render_template('profile.html', user=user)


@app.route('/my-account')
def my_account_details():
    """Show account details and allow user to make changes"""

    username = session.get('username')

    user = crud.get_user_by_username(username)

    return render_template('my-account.html', user=user)


def send_async_email(app, msg):
    """Makes the send email function asynchronous, in order to happen in the background """
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """Sends the email to user with a token"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

    
def send_password_reset_email(user):
    """Creates a token for the user and request the email to be sent"""
    
    secret = "jwt_secret"
    payload = {"exp": datetime.utcnow() + timedelta(minutes=5), "user_id": user.user_id}
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

    send_email('[iDreamAstronomy] Reset Your Password',
               sender='idreamastronomy@gmail.com',
                recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


@app.route('/forgot')
def forgot_password():
    """Shows the form to ask for the user username or email to request a new password"""

    username = session.get('username')

    if username in session:
        return redirect('/profile')
    
    return render_template('forgot_password.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_handle():
    """Handles the reset password form"""

    username = session.get('username')

    user_info = request.form.get('user_info_reset_password')

    user = crud.get_user_by_email_or_username(user_info)

    if user:
        send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect('/')
    if user is None:
        flash("Sorry, we could not find this email in our database")

    return redirect('/forgot')


@app.route('/forgot/new_password/')
def forgot_password_token():
    """Handles the new password process after being reset"""

    user_id = session.get('new_user_id')

    user = crud.get_user_by_id(user_id)

    if user is None:
        return redirect('/reset_password')

    if user:
        return render_template('reset_password.html')


@app.route('/forgot/change/<token>')
def check_token_valid(token):
    """Check if the token if valid or expired, and if its expired throws an error"""

    try:
        user_info = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"], verify_signature=True)
        new_user_id = user_info['user_id']
        session['new_user_id'] = new_user_id
        return redirect(url_for('forgot_password_token'))

    except jwt.ExpiredSignatureError:
        flash("Invalid or Expired Token, please get a new one.")
        return redirect('/')


@app.route('/forgot/change/new_password/', methods=['GET', 'POST'])
def create_new_password():
    """Creates a new password in database after being reset"""

    user_id = session.get('new_user_id')

    user = crud.get_user_by_id(user_id)

    new_password = request.form.get('new_password')
    new_password_conf = request.form.get('new_password_conf')

    if new_password != new_password_conf:
        flash("The passwords do not match")

    if new_password == new_password_conf:
        user.password = new_password
        db.session.commit()
        flash('Your password has been successfully changed. Please login')
        return redirect('/')
    
    return redirect('/forgot/new_password/')


@app.route('/change-password')
def change_password():
    """Display the form to change current password"""

    return render_template('change_password.html')


@app.route('/change-current-password')
def change_current_password():
    """Process the change of password in the database"""

    username = session.get('username')

    user = crud.get_user_by_username(username)

    current_password = request.args.get('current_password')

    new_password = request.args.get('new_password')

    repeat_new_password = request.args.get('repeat_new_password')

    if user.password != current_password:
        flash("The password you entered does not match our records, please try again or reset your password")
    if user.password == current_password:
        user.password = new_password
        db.session.commit()
        flash("password has been successfully updated!")
        return redirect('/profile')


    return redirect('/change-password')


@app.route('/change-acc-information')
def change_acc_information():
    """Display the form to change account information"""

    return render_template('change_acc_info.html')


@app.route('/change-account-info')
def change_account_info():
    """Process the change on account information in the database"""

    username = session.get('username')

    user = crud.get_user_by_username(username)

    users = crud.all_users()

    new_fname = request.args.get('new_fname')

    new_lname = request.args.get('new_lname')

    new_email = request.args.get('new_email')

    new_username = request.args.get('new_username')

    if new_fname:
        user.fname = new_fname
        db.session.commit()
        flash("The information you entered has been successfully updated!")
        return redirect('/profile')
    if new_lname:
        user.lname = new_lname
        db.session.commit()
        flash("The information you entered has been successfully updated!")
        return redirect('/profile')
    if new_email:
        try:
            user.email = new_email
            db.session.commit()
            flash("Your email has been successfully updated!")
            return redirect('/profile')
        except exc.IntegrityError:
            db.session.rollback()
            flash("Sorry, the email you entered is not available")
        
    if new_username:
        try:
            user.username = new_username
            db.session.commit()
            flash("Your username has been successfully updated!")
            return redirect('/profile')
        except exc.IntegrityError:
            db.session.rollback()
            flash("Sorry, the username you entered is not available")
    
    return redirect('/change-acc-information')


@app.route('/asteroids/selection')
def show_asteroids_selection():
    """Allows the user to select a date range to see asteroids"""

    return render_template('asteroids_selection.html')


@app.route("/asteroids")
def all_asteroids():
    """Show all asteroids"""

    start_date = request.args.get('asteroid_start_date')
    end_date = request.args.get('asteroid_end_date')

    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {'start_date': start_date, 
      'end_date': end_date, 
      'API_KEY': API_KEY
    }
    res = requests.get(url, params=params)
    neo_data = res.json()
  
    list_of_asteroids=[]

    for date in neo_data['near_earth_objects']:
        for asteroid in neo_data['near_earth_objects'][date]:

            asteroid_data_dict = {}

            asteroid_data_dict['api_asteroid_id'] = asteroid['neo_reference_id']
            asteroid_data_dict['name'] = asteroid['name']
            asteroid_data_dict['potentially_hazardous'] = asteroid['is_potentially_hazardous_asteroid']
            asteroid_data_dict['close_approach_date'] = asteroid['close_approach_data'][0]['close_approach_date_full']
            asteroid_data_dict['nasa_jpl_url'] = asteroid['nasa_jpl_url']
            asteroid_data_dict['relative_velocity_kilometers_per_hour'] = asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
            asteroid_data_dict['relative_velocity_miles_per_hour'] = asteroid['close_approach_data'][0]['relative_velocity']['miles_per_hour']
            asteroid_data_dict['orbiting_body'] = asteroid['close_approach_data'][0]['orbiting_body']
            asteroid_data_dict['miss_distance_kilometers'] = asteroid['close_approach_data'][0]['miss_distance']['kilometers']
            asteroid_data_dict['miss_distance_miles'] = asteroid['close_approach_data'][0]['miss_distance']['miles']
            asteroid_data_dict['estimated_diameter_kilometers_min'] = asteroid['estimated_diameter']['kilometers']['estimated_diameter_min']
            asteroid_data_dict['estimated_diameter_kilometers_max'] = asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']
            asteroid_data_dict['estimated_diameter_miles_min'] = asteroid['estimated_diameter']['miles']['estimated_diameter_min']
            asteroid_data_dict['estimated_diameter_miles_max'] = asteroid['estimated_diameter']['miles']['estimated_diameter_max']

            list_of_asteroids.append(asteroid_data_dict)

    return render_template("all_asteroids.html", list_of_asteroids=list_of_asteroids)


@app.route('/asteroids/<api_asteroid_id>')
def get_asteroid_details(api_asteroid_id):
    """View the details of an asteroid."""

    asteroid_details_dict = {}

    asteroid_details_dict['api_asteroid_id'] = request.args.get('api_asteroid_id')
    asteroid_details_dict['name'] = request.args.get('name')
    asteroid_details_dict['potentially_hazardous'] = request.args.get('potentially_hazardous')
    asteroid_details_dict['close_approach_date'] = request.args.get('close_approach_date')
    asteroid_details_dict['nasa_jpl_url'] = request.args.get('nasa_jpl_url')
    asteroid_details_dict['relative_velocity_kilometers_per_hour'] = request.args.get('relative_velocity_kilometers_per_hour')
    asteroid_details_dict['relative_velocity_miles_per_hour'] = request.args.get('relative_velocity_miles_per_hour')
    asteroid_details_dict['orbiting_body'] = request.args.get('orbiting_body')
    asteroid_details_dict['miss_distance_kilometers'] = request.args.get('miss_distance_kilometers')
    asteroid_details_dict['miss_distance_miles'] = request.args.get('miss_distance_miles')
    asteroid_details_dict['estimated_diameter_kilometers_min'] = request.args.get('estimated_diameter_kilometers_min')
    asteroid_details_dict['estimated_diameter_kilometers_max'] = request.args.get('estimated_diameter_kilometers_max')
    asteroid_details_dict['estimated_diameter_miles_min'] = request.args.get('estimated_diameter_miles_min')
    asteroid_details_dict['estimated_diameter_miles_max'] = request.args.get('estimated_diameter_miles_max')

    return render_template('asteroid-details.html', asteroid_details_dict=asteroid_details_dict)


@app.route('/apod')
def show_picture_of_the_day():
    """Show the astronomy picture of the day"""
    
    date = request.args.get('apod_date')

    url = "https://api.nasa.gov/planetary/apod"
    params = {'date': date, 'thumbs': 'thumbs', 'api_key': API_KEY}
    res = requests.get(url, params)
    apod = res.json()
    
    return render_template('apod.html', apod=apod)


@app.route("/delete-favorites", methods=["POST"])
def delete_favorite():
    """Deletes the favorite asteroid for that user"""

    user_id = session.get('user_id')

    user = crud.get_user_by_id(user_id)

    asteroid_id = request.form.get('asteroid_id')

    crud.delete_asteroid_by_user_id(user_id, asteroid_id)
    flash("This asteroid was successfully deleted!")
    
    return redirect('/my-journal')


@app.route("/save-favorites", methods=["POST"])
def save_favorites_asteroid():
    """Save favorite asteroid"""

    user_id = session.get('user_id')

    asteroid_details_dict = {}

    asteroid_details_dict['api_asteroid_id'] = request.form.get('api_asteroid_id')
    asteroid_details_dict['name'] = request.form.get('name')
    asteroid_details_dict['potentially_hazardous'] = request.form.get('potentially_hazardous')
    asteroid_details_dict['close_approach_date'] = request.form.get('close_approach_date')
    asteroid_details_dict['nasa_jpl_url'] = request.form.get('nasa_jpl_url')
    asteroid_details_dict['relative_velocity_kilometers_per_hour'] = request.form.get('relative_velocity_kilometers_per_hour')
    asteroid_details_dict['relative_velocity_miles_per_hour'] = request.form.get('relative_velocity_miles_per_hour')
    asteroid_details_dict['orbiting_body'] = request.form.get('orbiting_body')
    asteroid_details_dict['miss_distance_kilometers'] = request.form.get('miss_distance_kilometers')
    asteroid_details_dict['miss_distance_miles'] = request.form.get('miss_distance_miles')
    asteroid_details_dict['estimated_diameter_kilometers_min'] = request.form.get('estimated_diameter_kilometers_min')
    asteroid_details_dict['estimated_diameter_kilometers_max'] = request.form.get('estimated_diameter_kilometers_max')
    asteroid_details_dict['estimated_diameter_miles_min'] = request.form.get('estimated_diameter_miles_min')
    asteroid_details_dict['estimated_diameter_miles_max'] = request.form.get('estimated_diameter_miles_max')

    api_asteroid_id = request.form.get('api_asteroid_id')
    
    asteroid = crud.get_asteroid_by_api_id(api_asteroid_id)

    if asteroid == None:
        asteroid = crud.create_asteroid(api_asteroid_id=asteroid_details_dict['api_asteroid_id'], name=asteroid_details_dict['name'], potentially_hazardous=asteroid_details_dict['potentially_hazardous'], close_approach_date=asteroid_details_dict['close_approach_date'],
    nasa_jpl_url=asteroid_details_dict['nasa_jpl_url'], relative_velocity_kilometers_per_hour=asteroid_details_dict['relative_velocity_kilometers_per_hour'], relative_velocity_miles_per_hour=asteroid_details_dict['relative_velocity_miles_per_hour'], 
orbiting_body=asteroid_details_dict['orbiting_body'], miss_distance_kilometers=asteroid_details_dict['miss_distance_kilometers'], miss_distance_miles=asteroid_details_dict['miss_distance_miles'], 
estimated_diameter_kilometers_min=asteroid_details_dict['estimated_diameter_kilometers_min'], estimated_diameter_kilometers_max=asteroid_details_dict['estimated_diameter_kilometers_max'], 
estimated_diameter_miles_min=asteroid_details_dict['estimated_diameter_miles_min'], estimated_diameter_miles_max=asteroid_details_dict['estimated_diameter_miles_max'])
    
    list_of_favorites = crud.get_favorite_by_user_id(user_id)
    
    for favorite in list_of_favorites:
        if favorite.asteroids.api_asteroid_id == asteroid.api_asteroid_id:
            flash("This asteroid is already stored in your favorites")
            return redirect('/my-journal')
        
    favorite_asteroid = crud.create_favorite(user_id, asteroid.asteroid_id)

    return redirect('/my-journal')


@app.route("/my-journal/<int:api_asteroid_id>")
def favorite_asteroid_details(api_asteroid_id):
    """Display the favorite asteroids details"""

    asteroid = crud.get_asteroid_by_api_id(api_asteroid_id)

    return render_template('journal-details.html', asteroid=asteroid)


@app.route("/my-journal")
def personal_journal():
    """Display favorites asteroids for that user"""

    user_id = session.get('user_id')
    
    favorites = crud.get_favorite_by_user_id(user_id)

    return render_template('journal.html', favorites=favorites)


@app.route("/about")
def about():
    """Displays the about the developer section"""

    return render_template("about.html")


@app.route("/about_idreamastronomy")
def about_idreamastronomy():
    """Displays the about the developer section for no logged in user"""

    return render_template("about_no_login.html")


@app.route("/users", methods=['POST'])
def register_user():
    """Registers a new user in the database"""

    username = request.form.get('username')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    user = crud.get_user_by_username(username)

    if user:
        flash('Cannot create an account with that username and email. Try again')
    if password != confirm_password:
        flash("The password dont match, try again")
    if password == confirm_password:
        crud.create_user(username, fname, lname, email, password)
        flash('Account created! Please log in')

    return redirect('/')


@app.route('/log-in')
def log_user_in():
    """Logs the user in"""

    username = request.args.get('user_username')
    password = request.args.get("user_password")

    user = crud.get_user_by_username(username)

    if user and user.password == password:
        session['user_id'] = user.user_id
        session['username'] = username
        return redirect('/profile')
    if user and user.password != password and user.password is not None:
        flash("Wrong password, try again!")
    if user is None:
        flash("No account found with this username, please create an account first.")

    return redirect('/')


@app.route('/logout')
def logout():
    """Removes the user from the session"""

    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0')
    
