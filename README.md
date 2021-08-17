# iDreamAstronomy
iDreamAstronomy is a full stack web application that allows user to see asteroids that are orbiting earth as well as add it to a journal for later viewing.

Access the live webapp [here](http://idreamastronomy.com).

![Homepage](/static/img/gif/homepage.gif "Homepage")

## Contents
 - [Technologies](#technologies)
- [API](#api)
 - [Installation](#installation)
 - [About the Developer](#aboutthedeveloper)

### Technologies
* Python 3.7
* PostgresSQL
* Jinja
* Flask
* Flask-Mail
* JWT Token
* SQLAlchemy
* Javascript
* JQuery
* Semantic UI
* Bootstrap
* HTML/CSS

### <a name="api"></a> API
* [NASA's Open APIs](https://api.nasa.gov/) 
---
### Installation
#### Prerequisites
To run iDreamAstronomy, you must have installed:
 - [PostgreSQL](https://www.postgresql.org/)
 - [Python 3.7](https://www.python.org/downloads/)
 - [API key for NASA's APIs](https://api.nasa.gov/)
 - [Flask-Mail](https://pythonhosted.org/Flask-Mail/)
 - [JWT Token](https://jwt.io/)

 #### Run iDreamAstronomy on your local computer

 Clone or fork repository:
 ```
 $ git clone https://github.com/thalialietz/iDreamAstronomy
 ```

Create and activate a virtual environment within your iDreamAstronomy directory:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip3 install -r requirements.txt
$ pip3 install PyJWT
$ pip3 install Flask-Mail
```

Get an API key from NASA's Open APIs and add your API key to a secrets.sh file.

Run the secrets.sh file 
```
$ source secrets.sh
```

Run model.py to create all SQL database models
```
$ python3 model.py
```

Create database 'asteroidsdb':
```
$ createdb asteroidsdb
```

To run the app from the command line:
```
$ python3 server.py
```
---

### <a name="aboutthedeveloper"></a> About the Developer
iDreamAstronomy developer Thalia Lietz is a brazilian software engineer. This is her first full-stack project and was only possible with the support of her teachers at Hackbright Academy. She can be found on [LinkedIn](https://www.linkedin.com/in/thalialietz/) and on [Github](https://github.com/thalialietz).