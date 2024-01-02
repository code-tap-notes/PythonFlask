from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from os import path


app = Flask(__name__)
app.config["SECRET_KEY"]= "MyKey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.permanent_session_lifetime = timedelta(minutes=1)

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(app, model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html', name="Vien")

@app.route('/home')
def homePage():
    return render_template("home.html") 
@app.route('/list')
def list():
    users = User.query.order_by(User.username).all()
    return render_template("list.html",users = users) 
#@app.route('/users', methods = ['GET'])
#def get_users():
 #   all_users = User.query.all()
   # result = products_shema.dump(all_products)
    #return jsonify(result)
@app.route('/delete', methods=["POST","GET"])
def delete():
    user_name = request.form["name"]
    User.query.filter_by(username = user_name).delete()
    db.session.commit()
    flash("user deleted")
    return redirect(url_for("list")) 

@app.route('/login', methods=["POST","GET"])
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
        return redirect(url_for("user",user=user_name)) 
    if "user" in session:
        name = session["user"]
        flash("You have been already Logged in !","info")
        return redirect(url_for("user",user=name))
    return render_template("login.html") 


@app.route('/admin')
def admin():
    return f"<h2> Hello Admin of web ! </h2>"


@app.route('/user', methods=["POST","GET"])
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
        return redirect(url_for("login"))
    
@app.route('/logout')
def log_out():
    session.pop("user",None)
    flash("You have been already Logged out !","info")
    return redirect(url_for("login"))

if __name__=="__main__":
    #if not path.exists("user.db"):
     #   db.create_all(app=app)
      #  print ("Created database")
    #with app.app_context():
     #   db.create_all()


    app.run(debug=True)