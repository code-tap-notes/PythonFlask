from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta 
from flask_login import current_user


from blueprints.calculator.calculator import calculator_bp
from webmain import create_app


app = create_app()

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.permanent_session_lifetime = timedelta(minutes=1)
app.register_blueprint(calculator_bp,url_prefix="/calculler")


@app.route('/')
def admin():
    return render_template("base.html", user=current_user)


if __name__=="__main__":
   
    app.run(debug=True)