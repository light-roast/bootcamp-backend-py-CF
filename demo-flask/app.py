from flask import Flask, redirect, render_template, request, session, url_for, flash 
from functools import wraps
app = Flask(__name__)
app.secret_key = "akjalslkjasklajslkasj"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST": 
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again"
        else:
            session["logged_in"] = True
            flash("You were logged in.")
            return redirect(url_for("home"))
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    flash("You were logged out.")
    return redirect(url_for("welcome"))