from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta 
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
app.config["SECRET_KEY"]= "MyKey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def hello_world():
    return render_template('index.html', name="Vien")

@app.route('/home')
def homePage():
    return render_template("home.html") 

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        
        user_name = request.form["name"]
        session.permanent = True
        if user_name:
            session["user"] = user_name
            flash("Login successfully !","info")
            return redirect(url_for("user",user=user_name)) 
    if "user" in session:
        name = session["user"]
        flash("You have been already Logged in !","info")
        return redirect(url_for("user",user=name))
    return render_template("login.html") 


@app.route('/admin')
def admin():
    return f"<h2> Hello Admin of web ! </h2>"


@app.route('/user')
def user():
    if "user" in session:
        name = session["user"]
      
        render_template("user.html",user=name) 
    else:
        flash("You haven't been Logged in !","info")
        return redirect(url_for("login"))
    
@app.route('/logout')
def log_out():
    session.pop("user",None)
    flash("You have been already Logged out !","info")
    return redirect(url_for("login"))

if __name__=="__main__":
    if not path.exists("user.db"):
        db.create_all(app=app)
        print ("Created database")

    app.run(debug=True)