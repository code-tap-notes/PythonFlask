from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)
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
        if user_name:
            return redirect(url_for("hello_user",name = user_name))
    return render_template("login.html") 



@app.route('/admin')
def hello_admin():
    return f"<h2> Hello Admin of web ! </h2>"


@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    return f"<h2> Hello {name}! </h2>"

if __name__=="__main__":
    app.run(debug=True)