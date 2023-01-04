from flask_app import app
from flask import request, render_template, redirect, flash, session
from flask_app.models.user_model import User
from flask_app.models.product_model import Product
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register/form')
def register_form():
    return render_template('register.html')


@app.route('/register', methods = ["POST"])
def register_user():
    if not User.validator(request.form):
        return redirect('/register/form')
    if User.get_by_email(request.form):
        flash('Email already used', 'email')
        return redirect('/register/form')
    data = {
        **request.form,
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.create(data)
    return redirect("/welcome")

@app.route('/welcome')
def welcome():
    if not 'user_id' in session:
        return redirect('/')
    return render_template('dashboard.html', user = User.get_by_id({'id' : session['user_id']}), products = Product.get_all())

@app.route('/login', methods = ["POST"])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid Email/Password', 'log')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash('Invalid Email/Password*', 'log')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/welcome')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    if not 'user_id' in session:
        return redirect('/')
    user = User.get_by_id({'id' : session['user_id']})
    print(user.first_name)
    return render_template("profile.html", user = user)

@app.route('/edit/profile')
def edit_profile():
    if not 'user_id' in session:
        return redirect('/')
    return render_template("edit_profile.html", user = User.get_by_id({'id' : session['user_id']}))

@app.route('/update/profile', methods =["POST"])
def update_profile():
    if not User.edit_validator(request.form):
        return redirect('/edit/profile')
    data = {
        'id': session['user_id'],
        **request.form
    }
    User.update(data)
    return redirect("/profile")

@app.route('/edit/password')
def edit_password():
    if not 'user_id' in session:
        return redirect('/')
    return render_template("edit_password.html", user = User.get_by_id({'id' : session['user_id']}))

@app.route('/update/password', methods =["POST"])
def update_pass():
    if not User.password_validator(request.form):
        return redirect('/edit/password')
    data = {
        'id': session['user_id'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    User.update_password(data)
    return redirect("/profile")