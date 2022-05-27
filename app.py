"""
    WEATHER APPLICATION 
    
    
    Requirements : 
            sqlite3 Database having two tables
                    users(name, password, email)
                    city(username, city)
                    
            API key of OpenWeather API
            Flask Module
           
"""

from flask import Flask
from flask import render_template
from datetime import datetime
from flask import request
from flask import escape
from openweather import get_temp
from flask import session
from flask import redirect
from flask import flash
import sqlite3
import os

PROJECT_DIR = os.path.abspath(".")

app = Flask(__name__)
app.secret_key = "justarandomstringtoencryptsessiondata"

def get_db():
    path = os.path.join(PROJECT_DIR, "weather.db")
    db = sqlite3.connect(path)
    return db

def get_date():
    return datetime.now().strftime("%A %d-%m-%Y %I:%M %p")


@app.route("/", methods=["GET"])
def index():
    if ("username" in session) and session["username"]:
        db = get_db()
        cur = db.execute("SELECT * FROM city WHERE username=?", (session["username"],))
        result = cur.fetchall()
        cities = [x[1] for x in result]
        data = []
        for city in cities:
            data.append(get_temp(city))
        return render_template("index.html",date=get_date(), cities=data)
    else:
        return render_template("login.html") 

    # if "city_names" not in session:
    #     session["city_names"] = []
    # cities = []
    # for city in session['city_names']:
    #     value = get_temp(city)
    #     if value:
    #        cities.append(value)
    #     else:
    #         session["city_names"].remove(city)
    #         session.modified = True
    # return render_template("index.html", date=get_date(), cities=cities)


@app.route("/", methods=["POST"])
def add_city():
    city = request.form.get("city").lower().strip()
    if ("username" in session) and session['username']:
        db = get_db()
        cur = db.execute("SELECT city FROM city WHERE username=?", (session["username"],))
        result = cur.fetchall()
        #(,)
        # (("jaipur", ), ("ajmer", ), ("tonk", ) )
        result = [ x[0] for x in result ]
        # [ "jaipur", "ajmer", "tonk"]
        if city not in result:
            cur = db.execute("INSERT INTO city VALUES (?, ?)", (session["username"], city))
            db.commit()
            flash(f'{city} added to table sucessfully!')
        db.close()
        return redirect("/")
    # if ("city_names" in session) and (city not in session["city_names"]):
    #     session["city_names"].append(city)
    #     session.modified = True
    # return redirect("/")
    # #value = get_temp(city)
    #if value:
    #    return render_template("index.html", data=value, date=get_date())
    #return "your data is here in python."


@app.route("/del_city/<name>")
def del_city(name=None):
    if (name) and ("username" in session):
        db = get_db()
        cur = db.execute("SELECT * FROM city WHERE username=?", (session["username"],))
        result = cur.fetchall()
        result = [ x[1] for x in result]
        if name in result:
            db.execute("DELETE FROM city WHERE city=?", (name, ))
            db.commit()
            flash(f"{name} city delete successfully!")
        db.close()
        # session['city_names'].remove(name)
        # session.modified = True
    return redirect("/")


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    name = escape(request.form.get("user").lower().strip())
    password = escape(request.form.get("passwd"))
    email = escape(request.form.get("email"))
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE name=? OR email=?", (name, email))
    result = cur.fetchall()
    if len(result) == 0:
        # user does not exists
        db.execute("INSERT INTO users(name, password, email) VALUES (?, ?, ?)", (name, password, email))
        db.commit()
        db.close()
        flash("Account Created Successfully!")
        return redirect("/login")
    else:
        flash("Username or Email Already Exists Please Login! or Signup up with Diffrent Username or Email")
        return redirect("/login")
        # user exists already

    return f"<h3>you are trying to create a user with data {name} {password} {email}</h3>"

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
        flash("Sucessfully Logged out!")
        return redirect("/")
    else:
        flash("you are not logged in!")
        return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signin", methods=["POST"])
def signin():
    name = escape(request.form.get('user').strip().lower())
    passwd = escape(request.form.get('passwd'))
    # check user exists or not
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE name=?", (name, ))
    result = cur.fetchall()
    db.close()
    if len(result) == 0:
        flash(f"account with {name} username does not exists check username or !Signup! if you do not have an account!")
        return redirect("/signup")
    else:
        user = result[0] # ((name, password, email), )
        if passwd == user[1]:
            session["username"] = name
            return redirect("/")
        else:
            flash("Incorrect Password!Try Again!!")
            return redirect("/login")
   
   
@app.route("/hello/<string:name>")
def hello(name=None):
    return f"Hello {name} Welcome to Python!"

if __name__ == "__main__":
    # 192.168.29.211
    app.run("0.0.0.0", 80, debug=True)
    # error page -> descriptive error so that we can debug error eaisly
    # we do need to re-run over server again and again after changing website
