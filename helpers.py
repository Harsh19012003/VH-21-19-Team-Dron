import os
import requests
import urllib.parse
import json 

import pandas as pd

from flask import redirect, render_template, request, session
from functools import wraps


# Apology renders memetemplate as an userside error
def apology(message, code=400):
    # Render message as an apology to user.
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Function used above every other function which ensures user is logged in
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Function inserts symbol to url which inturn returns all info about that stock
def lookup(symbol):
    # Look up quote for symbol.

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


# Functions which converts float to usd
def usd(value):
    # Format value as USD.
    return f"${value:,.2f}"


# Checks password requirements
def password_check(ps):
    # Ensures password contains atleast one uppercase, one lowercase, one numeric.
    uc = False
    lc = False
    nm = False
    print(type(uc))
    for char in ps:
        if char.isupper():
            uc = True
        if char.islower():
            lc = True
        if char.isdigit():
            nm = True

    if uc and lc and nm:
        return True
    else:
        return False

def user_location():
    request_url = 'https://geolocation-db.com/jsonp/'
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result  = json.loads(result)
    print(result)
    return result

def lookdata():
    # Contact API
    try:
        url = f"https://wittypanda.github.io/data_api/csvjson.json"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()
        return data
    except (KeyError, TypeError, ValueError):
        return None

dt = pd.read_csv('Database2.csv', sep=",")

keywords = ["Mumbai"]
searched_keywords = '|'.join(keywords)

branch = ["Computer Engineering"]
searched_branch = '|'.join(branch)


cutoff = ["83.35"]
cut = pd.to_numeric(cutoff)
searched_cutoff = '|'.join(cutoff)

# read the csv data into a dataframe 
# change "," to the data separator in your csv file 
#df = pd.read_csv("2006-data-8-8-2016.csv", sep=",")
# filter the data: keep only the rows that contain one of the keywords 
# in the position or the Job description columns
#data = data[data["Institute"].str.contains(searched_keywords) | data["Institute"].str.contains(searched_keywords)] 
# write the data back to a csv file 
#data.to_csv("Sl1.csv",sep=",", index=False) 


import csv
import json

csvfile = open('Database2.csv', 'r')
jsonfile = open('file.json', 'w')

fieldnames = ("Sr.No","Rank","CUTOFF","Institute Name","Exam")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
