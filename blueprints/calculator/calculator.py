from flask import Blueprint, render_template, redirect, url_for
calculator_bp = Blueprint("calculator", __name__,template_folder="templates")
@calculator_bp.route("/")
def index():
    return "This ia calculator blusprint"

@calculator_bp.route("/add/<int:n1>/<int:n2>")
def add(n1,n2):
    return str(n1+n2)

@calculator_bp.route("/return")
def return_home():
    return redirect(url_for("homePage"))