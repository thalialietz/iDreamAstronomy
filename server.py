from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash)
from model import db, connect_to_db
import crud
import os
import requests
import json

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

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

    if user.password != current_password:
        flash("The password you entered does not match our records, please try again")
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

    new_fname = request.args.get('new_fname')

    new_lname = request.args.get('new_lname')

    new_email = request.args.get('new_email')

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
        user.email = new_email
        db.session.commit()
        flash("The information you entered has been successfully updated!")
        return redirect('/profile')

    return redirect('/change-acc-information')


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


@app.route("/my-journal")
def personal_journal():
    """Display favorites asteroids for that user"""

    user_id = session.get('user_id')
    
    favorites = crud.get_favorite_by_user_id(user_id)

    return render_template('journal.html', favorites=favorites)


@app.route("/users", methods=['POST'])
def register_user():
    """Registers a new user in the database"""

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
    """Logs the user in"""

    username = request.args.get('user_username')
    password = request.args.get("user_password")

    user = crud.get_user_by_username(username)
    
    if user and user.password == password:
        session['user_id'] = user.user_id
        session['username'] = username
        return redirect('/profile')
    if user and user.password != password:
        flash("Wrong password, try again!")
    else:
        flash("No account found with this username, please create an account first.")

    return redirect('/')


@app.route('/logout')
def logout():
    """Removes the user from the session"""

    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0')
    
