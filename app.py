"""
    WEATHER APPLICATION


    Requirements :
            sqlite3 Database having two tables
                    users(name, password, email)
                    city(username, city)

            API key of OpenWeather API
            Flask Module

"""
from datetime import datetime
import sqlite3
import os
from flask import Flask
from flask import render_template
from flask import request
from flask import escape
from flask import session
from flask import redirect
from flask import flash
from openweather import get_temp

PROJECT_DIR = os.path.abspath(".")

app = Flask(__name__)
app.secret_key = "justarandomstringtoencryptsessiondata"

def get_db():
    """
    connect to database file 'weather.db'
    using sqlite3 database engine
    """
    path = os.path.join(PROJECT_DIR, "weather.db")
    db_ = sqlite3.connect(path)
    return db_

def get_date():
    """
    returns date, time, day
    """
    return datetime.now().strftime("%A %d-%m-%Y %I:%M %p")


@app.route("/", methods=["GET"])
def index():
    """
    gets homepage for the user in session
    """
    if ("username" in session) and session["username"]:
        db_ = get_db()
        cur = db_.execute("SELECT * FROM city WHERE username=?", (session["username"],))
        result = cur.fetchall()
        cities = [x[1] for x in result]
        data = []
        for city in cities:
            data.append(get_temp(city))
        return render_template("index.html",date=get_date(), cities=data)

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
    """
    adds city for user in database file
    """
    city = request.form.get("city").lower().strip()
    if ("username" in session) and session['username']:
        db_ = get_db()
        cur = db_.execute("SELECT city FROM city WHERE username=?", (session["username"],))
        result = cur.fetchall()
        #(,)
        # (("jaipur", ), ("ajmer", ), ("tonk", ) )
        result = [ x[0] for x in result ]
        # [ "jaipur", "ajmer", "tonk"]
        if city not in result:
            cur = db_.execute("INSERT INTO city VALUES (?, ?)", (session["username"], city))
            db_.commit()
            flash(f'{city} added to table sucessfully!')
        db_.close()
        return redirect("/")
    return None
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
    """
    deletes city not required by user from database file
    """
    if (name) and ("username" in session):
        db_ = get_db()
        cur = db_.execute("SELECT * FROM city WHERE username=?", (session["username"],))
        result = cur.fetchall()
        result = [ x[1] for x in result]
        if name in result:
            db_.execute("DELETE FROM city WHERE city=?", (name, ))
            db_.commit()
            flash(f"{name} city delete successfully!")
        db_.close()
        # session['city_names'].remove(name)
        # session.modified = True
    return redirect("/")


@app.route("/signup")
def signup():
    """
    returns template 'signup.html'
    """
    return render_template("signup.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    """
    saves user details in database file 'weather.db'
    """
    name = escape(request.form.get("user").lower().strip())
    password = escape(request.form.get("passwd"))
    email = escape(request.form.get("email"))
    db_ = get_db()
    cur = db_.execute("SELECT * FROM users WHERE name=? OR email=?", (name, email))
    result = cur.fetchall()
    if len(result) == 0:
        # user does not exists
        db_.execute("INSERT INTO users(name, password, email) VALUES (?, ?, ?)",\
        (name, password, email))
        db_.commit()
        db_.close()
        flash("Account Created Successfully!")
        return redirect("/login")

    flash("Username or Email Already Exists Please Login! or\
     Signup up with Different Username or Email")
    return redirect("/login")

@app.route("/logout")
def logout():
    """
    session is stopped and user details are removed from the new session
    """
    if "username" in session:
        session.pop("username")
        flash("Sucessfully Logged out!")
        return redirect("/")

    flash("you are not logged in!")
    return redirect("/")

@app.route("/login")
def login():
    """
    returns template 'login.html'
    """
    return render_template("login.html")

@app.route("/signin", methods=["POST"])
def signin():
    """
    checks user validity and authenticates user
    for a session
    """
    name = escape(request.form.get('user').strip().lower())
    passwd = escape(request.form.get('passwd'))
    # check user exists or not
    db_ = get_db()
    cur = db_.execute("SELECT * FROM users WHERE name=?", (name, ))
    result = cur.fetchall()
    db_.close()
    if len(result) == 0:
        flash(f"account with {name} username does not exists check username or\
         !Signup! if you do not have an account!")
        return redirect("/signup")

    user = result[0] # ((name, password, email), )
    if passwd == user[1]:
        session["username"] = name
        return redirect("/")

    flash("Incorrect Password!Try Again!!")
    return redirect("/login")

@app.route("/hello/<string:name>")
def hello(name=None):
    """
    welcomes the <name> user at route '/hello/<name>'
    """
    return f"Hello {name} Welcome to Python!"

if __name__ == "__main__":
    # 192.168.29.211
    app.run("0.0.0.0", 80, debug=True)
    # error page -> descriptive error so that we can debug error eaisly
    # we do need to re-run over server again and again after changing website
