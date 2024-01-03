from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta 
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from os import path
from flask.blueprints import Blueprint

user_bp = Blueprint("user", __name__)
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(user_bp, model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
with user_bp.app_context():
    db.create_all()

@user_bp.route('/list')
def list():
    users = User.query.order_by(User.username).all()
    return render_template("list.html",users = users) 
#@app.route('/users', methods = ['GET'])
#def get_users():
 #   all_users = User.query.all()
   # result = products_shema.dump(all_products)
    #return jsonify(result)
@user_bp.route('/delete', methods=["POST","GET"])
def delete():
    user_name = request.form["name"]
    User.query.filter_by(username = user_name).delete()
    db.session.commit()
    flash("user deleted")
    return redirect(url_for("user.list")) 

@user_bp.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
       
        user_name = request.form["name"]
        session.permanent = True
        if user_name:
            session["user"] = user_name
            found_user = User.query.filter_by(username = user_name).first()
            if found_user:
              session["email"] = found_user.email
            else:   
                user = User(user_name,"temp@gmail.com")
                db.session.add(user)
                db.session.commit()
            flash("Login successfully ! add to database","info")
        return redirect(url_for("user.user",user=user_name)) 
    if "user" in session:
        name = session["user"]
        flash("You have been already Logged in !","info")
        return redirect(url_for("user.user",user=name))
    return render_template("login.html") 


@user_bp.route('/admin')
def admin():
    return f"<h2> Hello Admin of web ! </h2>"


@user_bp.route('/user', methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        name = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = User.query.filter_by(username = name).first()
            found_user.email = email
            db.session.commit()
            flash("email updated")
        elif "email" in session:
            email = session["email"]
        return render_template("user.html",user=name, email = email) 
    else:
        flash("You haven't been Logged in !","info")
        return redirect(url_for("user.login"))
    
@user_bp.route('/logout')
def log_out():
    session.pop("user",None)
    flash("You have been already Logged out !","info")
    return redirect(url_for("user.login"))
