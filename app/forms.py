from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import (InputRequired, Length, Email, EqualTo,
 ValidationError, NumberRange, InputRequired)
from app.models import User, Food

'''
Form to add a new product to the database
'''
class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=60)])
    description = StringField('Description', validators=[InputRequired(), Length(max=300)])
    quantity = IntegerField('Quantity of stock', validators=[InputRequired(), NumberRange(min=0, max=100)])
    cost = IntegerField('Cost', validators=[InputRequired(), NumberRange(min=1, max=100)])
    department = StringField('Department', validators=[InputRequired(), Length(max=20)])
    image_file = FileField('Product Picture', validators=[InputRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Add Product')

    def validate_name(self, name):
        food = Food.query.filter_by(name=name.data).first()
        if food:
            raise ValidationError('This product name is already taken. Product may already be listed')

'''
Form to remove product in the database
'''
class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=60)])
    description = StringField('Description', validators=[Length(max=300)])
    quantity = IntegerField('Quantity of stock', validators=[NumberRange(min=0, max=100)])
    cost = IntegerField('Cost', validators=[NumberRange(min=1, max=100)])
    department = StringField('Department', validators=[Length(max=20)])
    image_file = FileField('Product Picture', validators=[FileAllowed(['jpg', 'jepg', 'png'])])
    submit = SubmitField('Update Product')

    def validate_name(self, name):
        if name.data != food.name:
            food = Food.query.filter_by(name=name.data).first()
            if food:
                raise ValidationError('This product name is already taken. Product may already be listed')

'''
Form to remove product in the database
'''
class RemoveProductForm(FlaskForm):
    submit = SubmitField('Remove Product')


'''
Retistration Form to create a username, email, password, and confirm password
'''
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=32)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken.')

'''
Login Form to login to previously registered account
'''
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=32)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

'''
Account Form to update account information
'''
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[Length(max=30)])
    last_name = StringField('Last Name', validators=[Length(max=30)])
    state = StringField('State', validators=[Length(max=2)])
    city = StringField('City', validators=[Length(max=30)])
    address = StringField('Address', validators=[Length(max=30)])
    zip_code = StringField('ZIP Code', validators=[Length(min=5, max=5)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken.')

'''
Request Form to request a password reset
'''
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Request Password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no registered account with that Email')

'''
Reset Form to change a password
'''
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=32)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

'''
Billing Address and Payment form for Cart page
'''
class BillingForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])
    state = StringField('State', validators=[InputRequired(), Length(max=2)])
    city = StringField('City', validators=[InputRequired(), Length(max=30)])
    address = StringField('Address', validators=[InputRequired(), Length(max=30)])
    zip_code = StringField('ZIP Code', validators=[InputRequired(), Length(min=5, max=5)])
    submit = SubmitField('Checkout')

    def validate_zip(self, zip_code):
        if zip_code is False:
            raise ValidationError('No zip')
