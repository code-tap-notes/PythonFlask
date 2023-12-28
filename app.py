from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html', name="Vien")


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