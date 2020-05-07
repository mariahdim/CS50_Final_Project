import os
import requests
import json
import pandas as pd

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta, date
from urllib.request import urlopen

from helpers import apology, login_required, unique, menu, food, get_soup, get_lunch, get_dinner, get_dessert

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///huds.db")

# # Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

@app.route("/")
def home():

    # we want do display the menu for the upcoming week:
    span = 7
    # Initialize empty vectors
    dates = [None] * span
    nice_dates = []
    soups = [None] * span
    lunches = [None] * span
    dinners = [None] * span
    dessert_lunches = [None] * span
    dessert_dins = [None] * span
    # Textual month, day and year (for display in jumbotron)
    d8 = datetime.today()
    d = d8.strftime("%b. %d, %Y")

    for i in range(span):
        x = d8 + timedelta(days=i)
        date = x.date()
        dates.append(date)
        nice_dates.append(date.strftime('%B %d'))

        ## SOUP OF THE DAY
        soup = get_soup(date)
        soups[i] = unique(soup)
        # soup = pd.DataFrame(unique(soup))
        # soups[i] = soup.to_html()

        ## ENTREES
        lunch = get_lunch(date)
        lunches[i] = unique(lunch)

        dinner = get_dinner(date)
        dinners[i] = unique(dinner)

        # DESSERT
        dessert_lunch = get_dessert(date, meal=1)
        dessert_lunches[i] = unique(dessert_lunch)

        dessert_din = get_dessert(date, meal=2)
        dessert_dins[i] = unique(dessert_din)

    return render_template("home.html", dates=dates, nice_dates=nice_dates, soups=soups, lunches=lunches, dinners=dinners, dessert_lunches=dessert_lunches, dessert_dins=dessert_dins, d=d)

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get username
    username = request.args.get("username")

    # Check for username
    if not len(username) or db.execute("SELECT 1 FROM users WHERE username = :username", username=username.lower()):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/ratings")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/ratings", methods=["GET", "POST"])
@login_required
def ratings():
    """Ratings of the food of the day."""

    # POST
    if request.method == "POST":

        id = db.execute("INSERT INTO ratings (soup, lunch, dinner) VALUES(:soup, :lunch, :dinner)",
                        soup=request.form.get("soup"),
                        lunch=request.form.get("lunch"),
                        dinner=request.form.get("dinner"))

        flash("Ratings saved!")
        return redirect("/")

    # GET
    else:
        return render_template("ratings.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                        username=request.form.get("username"),
                        hash=generate_password_hash(request.form.get("password")))
        if not id:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)

# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)