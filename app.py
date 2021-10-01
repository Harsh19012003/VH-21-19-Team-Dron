import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, password_check, user_location, lookdata

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.jinja_env.filters["usd"] = usd

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = sqlite3.connect("database.db")
db = conn.cursor()

try:
    sqliteConnection = sqlite3.connect('database.db', check_same_thread=False)
    db = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    db.execute(sqlite_select_Query)
    record = db.fetchall()
    print("SQLite Database Version is: ", record)
    

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)


print("table succesfull")

data = lookdata()
print(data)

"""
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    # Log user in

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        rows = db.fetchall()
        print("BBBBBBBBB")
        print(rows)
        #rows[""]
        # Ensure username exists and password is correct
        a = request.form.get("password") 
        # or not check_password_hash(rows[0]["hash"] == 
        if len(rows) != 1:
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        print("AAAAAAAAAAAAAAAAAAAAAAAa")
        db.execute("SELECT * FROM users")
        print(db.fetchall())

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Register user

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Creat variables
        username = request.form.get("username")
        #type(username)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("confirmation")

        # Ensure user has written username
        if not username:
            return apology("Must provide Username", 400)

        # Ensure no other user is in database with same username
        db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = db.fetchall()
        print(f"TYPE : ...............{type(rows)}")
        if len(rows) != 0:
            return apology("Username is already taken")

        # Ensure user has written password
        if not password:
            return apology("Must provide password", 400)

        # Ensure user has written confirmation of password
        if not confirmation:
            return apology("Must provide confirmation", 400)

        # Ensure password in both fields(password and confirmation) is same
        if password != confirmation:
            return apology("Password and Confirmation donot match")

        # Ensure password satisfies the requirements of one uppercase, one lowercase, one numeric and one symbol
        ps = list(password.strip(" "))
        requirement = password_check(ps)
        if requirement == False:
            return apology("Password Requirement")

        # Register user by storing it in database. Here, javascript can be added.
        db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", [username, generate_password_hash(password), email])
        return redirect("/")

    # User reached route via GET (as by clicking a link)
    else:
        return render_template("register.html")

@app.route("/details", methods=["GET", "POST"])
def details():
    # Accept user details

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        hsc_score = request.form.get("hsc_score")
        jee_cet_score = request.form.get("jee_cet_score")
        p1 = request.form.get("p1")
        p2 = request.form.get("p2")
        p3= request.form.get("p3")

        iplocation = user_location()
        print(iplocation)
        return redirect("/")
    
    else:
        iplocation = user_location()
        print(iplocation)
        return render_template("details.html")

@app.route("/logout")
def logout():
    # Log user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

app.run(debug=True)