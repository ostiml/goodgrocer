import os
import secrets
from PIL import Image
from flask import render_template, url_for, request, flash, redirect
from app import app, db, bcrypt, mail
from app.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
 RequestResetForm, ResetPasswordForm, BillingForm, AddProductForm, EditProductForm,
 RemoveProductForm)
from app.models import User, Food
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

'''
Route to index page
'''
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', food=Food.query.all())

'''
Route to register page. Users can register an account with four fields: Username,
Email, Password, Confirm Password. Password hashed using Bcrypt
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

'''
Route to login page. Users can login with Username and Password. Password hash
checked using Bcrypt.
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Login successful! You are now logged in','success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password','danger')
    return render_template('login.html', title='Login', form=form)

'''
Route to logout page
'''
@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successful! You are now logged out','info')
    return redirect(url_for('index'))

'''
Route to account page. Must be logged in to access account page. Account page
used to update account information
'''
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.state = form.state.data
        current_user.city = form.city.data
        current_user.address = form.address.data
        current_user.zip_code = form.zip_code.data
        db.session.commit()
        flash('Your account has been updated', 'info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.state.data = current_user.state
        form.city.data = current_user.city
        form.address.data = current_user.address
        form.zip_code.data = current_user.zip_code
    return render_template('account.html', title='Account', form=form)

'''
Route to user's item cart
'''
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    form = BillingForm()
    if form.validate_on_submit(): #SHOULD UPDATE CART/ ORDER MODEL
        flash('Your order has been placed. A confirmation email has been sent to you', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.state.data = current_user.state
        form.city.data = current_user.city
        form.address.data = current_user.address
        form.zip_code.data = current_user.zip_code
    return render_template('cart.html', title='Cart', form=form)

'''
Route to guest's item cart
'''
@app.route('/guestcart', methods=['GET', 'POST'])
def guestcart():
    form = BillingForm()
    if current_user.is_authenticated:
        return redirect(url_for('cart'))
    elif form.validate_on_submit():
        flash('Your order has been placed. A confirmation email has been sent to you', 'success')
        return redirect(url_for('index'))
    return render_template('cart.html', title='Guest Cart', form=form)

'''
Route to view a product in depth
'''
@app.route('/product') ###NEEDS TO BE FIXED
def product():
    return render_template('product.html', title='product', food=Food.query.all())

'''
Method to save picture from image_file
'''
def save_image(image_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image_file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/newimages', picture_fn)


    output_size = (400, 300)
    i = Image.open(image_file)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

'''
Route to edit or remove prooducts to the website
'''
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    ''' add a product'''
    addform = AddProductForm()
    if addform.validate_on_submit():
        if addform.image_file.data:
            image = save_image(addform.image_file.data)
        food = Food(name=addform.name.data, cost=addform.cost.data,
         description=addform.description.data, quantity=addform.quantity.data,
          department=addform.department.data, image_file=image)
        db.session.add(food)
        db.session.commit()
        flash('Product has been updated', 'info')
    '''remove a product'''
    removeform = RemoveProductForm()

    '''modify an existing product'''
    editform = RemoveProductForm()
    image_file = url_for('static', filename='newimages/' + Food.image_file)
    return render_template('inventory.html', title='product', food=Food.query.all(),
     image_file=image_file, addform=addform, removeform=removeform, editform=editform)

'''
Route to request password reset page and recieve token
'''
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent with instructions to reset your Password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

'''
Route to reset password using token
'''
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or expired. Request a new one', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your Password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

'''
Send user a reset password email
'''
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='jessebaby313@gmail.com',
    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes
 will be made.
 ***THIS IS A EDUCATION AND DEMONSTRATION PROJECT ONLY. DO NOT
 STORE SENSITIVE INFORMATION HERE***
'''
    mail.send(msg)
