from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta 

app = Flask(__name__)
app.config["SECRET_KEY"]= "MyKey"
app.permanent_session_lifetime = timedelta(minutes=1)
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
            return render_template("user.html",user=user_name) 
    if "user" in session:
        name = session["user"]
        flash("You have been already Logged in !","info")
        return render_template("user.html",user=name) 
    return render_template("login.html") 



@app.route('/admin')
def hello_admin():
    return f"<h2> Hello Admin of web ! </h2>"


@app.route('/user')
def hello_user():
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
    app.run(debug=True)