from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        print(email)
        if user:
            if check_password_hash(user.password,password):
                flash('Login successfully !',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password !',category='error')
                return render_template("login.html")   
        else:
            flash('Email is not exsist !',category='error')
            return redirect(url_for('auth.sign_up'))
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/list', methods=['GET','POST'])
def list():
    return render_template("list.html")

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email = email).first()
        if user:
             flash('email already exsists !',category='error')
        else:
            if len(email) <4:
                flash('Email must be greater than 4 characters', category='error')
             
            elif len(firstName) <2:
                flash('First Name must be greater than 1 characters', category='error')
             
            elif password1 != password2:
                flash('Password  don\'t match', category='error')
             
            elif len(password1) <7:
             flash('Password must be greater than 7 characters', category='error')
             
            else:
            #add to data base
                flash('Account created', category='success')
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256')) 
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template("sign_up.html",  user=current_user)