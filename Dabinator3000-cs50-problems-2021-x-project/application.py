import os

import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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
db = SQL("sqlite:///project.db")



@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":

        if request.args.get('Xc'):  # gets save highscore request for classic game
            current_user = session["user_id"]
            username = db.execute("SELECT username FROM users WHERE id=:id",id=current_user)
            x = username

            z = x[0]['username']
            print("--------------c----------",z,"-------c-----------------")
            score =  request.args.get('Xc')
            add_score = db.execute("INSERT into highscore_c (userid,username,score,date) VALUES(:userid,:username1,:score,CURRENT_DATE)",
            userid=current_user,username1=z,score=score)

        if request.args.get('Xr'):  # gets save highscore request for rapid game
            current_user = session["user_id"]
            username = db.execute("SELECT username FROM users WHERE id=:id",id=current_user)
            x = username

            z = x[0]['username']
            print("---------------r---------",z,"---------------r---------")
            score =  request.args.get('Xr')
            add_score = db.execute("INSERT into highscore_r (userid,username,score,date) VALUES(:userid,:username1,:score,CURRENT_DATE)",
            userid=current_user,username1=z,score=score)

        return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/suggestion", methods=["GET", "POST"])  # suggestion box for user's suggestion: currently it reaches "contact@yourdomain.com"
@login_required
def suggestion():
    if request.method == "POST":
        email = request.form.get("email")
        text = request.form.get("text")

        return render_template("suggestion.html")
    else:
        return render_template("suggestion.html")


@app.route("/highscore", methods=["GET", "POST"]) # To view highscores of user's previous games
@login_required
def highscore():
    if request.method == "GET":
        score_c = db.execute("SELECT * FROM highscore_c ORDER BY score ASC")
        print(score_c)



        score_r = db.execute("SELECT * FROM highscore_r ORDER BY score DESC")
        print(score_r)
        return render_template("highscore.html",score_c=score_c,score_r=score_r)

    else:
        return render_template("highscore.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("Please enter your username", 400)
        unique = db.execute("SELECT * FROM users WHERE username=:user",user=request.form.get("username"))
        if unique:
            return apology("Please enter your unique username", 400)
        if not request.form.get("password"):
            return apology("Please enter your password", 400)
        if not request.form.get("confirmation"):
            return apology("Please enter your confirmation password", 400)
        if (request.form.get("password") != request.form.get("confirmation")):
            return apology("Please enter matching passwords", 400)

        hash_password = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username,hash) VALUES (:username,:hash_p)", username = request.form.get("username"), hash_p = hash_password)

        return redirect("/login")



    else:
        return render_template("register.html")