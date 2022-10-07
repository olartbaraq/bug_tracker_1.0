#!/usr/bin env python3


# Copyright (c) Akanbi Mubaraq Olatunde. Aspiring back-end developer


"""
Some important modules are to be imported to make the flask-sqlalchemy work
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# this creates an instance of the Flask module imported from flask package
app = Flask(__name__)

# this set the database used to the in-built sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugtracker3.db'

# this is necessary to be set in order for wtforms
# with http methods to function
app.config['SECRET_KEY'] = '277aca85092d962dda58178e'

# this set the instance app to make use of sqlalchemy
# as an ORM to store data to sqlite3 database
db = SQLAlchemy(app)

# this helps hash the password inputted to the form
# not to be stored as a plain text in the database
# bcrypt = Bcrypt(app)

# this set the app instance as an instance of LoginManager
# for a user to sign-in the website using their credentials
# that has been stored on the database
# login_manager = LoginManager(app)

# login_manager.login_view = "sign_in"

# this set the flash message to display the key:value
# pairs of information regarding sign-in of a user
# login_manager.login_message_category = 'info'


from main_files import all_routes

# this makes it easy to prevent circular imports of modules from
# all_routes.py file to access the above instances and variables
