import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

'''
Flask
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b5adfcf1cd2c3dddb80dec510dfade59'

'''
Database configurations
'''
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

'''
Bcrypt for password hashing
'''
bcrypt = Bcrypt(app)

'''
Login configurations
'''
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

'''
Mail configurations
'''
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('GoodGrocerMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('GoodGrocerMAIL_PASS')
mail = Mail(app)

from app import routes
