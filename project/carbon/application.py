import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError
from flask_mail import Mail, Message
from helpers import apology, login_required, usd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# some source code based on noa's code from cs50 finance
# as well as the cs50 finance distribution code


# Configure application
app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "carbonfootprintcs50@gmail.com"
mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///carbon.db")


@app.route("/")
def welcome():
   # Welcome page with info about what the site does and links to login, register, and calculate

    return render_template("welcome.html")


@app.route("/log", methods=["GET", "POST"])
@login_required
def log():
    # Log your daily carbon emissions

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Calculate and log carbon emissions
        user_id = db.execute("SELECT id FROM users WHERE id = ?", session["user_id"])
        user_id = user_id[0]["id"]
        driving_miles = int(request.form.get("drive"))
        shower_min = int(request.form.get("shower"))
        light_hours = int(request.form.get("light")) * int(request.form.get("rooms"))

        # calculate carbon from food
        food_carbon = round(6*int(request.form.get("beef")) + 9*int(request.form.get("lamb")) + 2*int(request.form.get("turkey")) + 2*int(
            request.form.get("tuna")) + 2*int(request.form.get("chicken")) + int(request.form.get("cheese")) + 3*int(request.form.get("pork")), 2)

        # calculate the total carbon emissions (all in kg)
        total_carbon = round(food_carbon + .12 * driving_miles + .1 * light_hours + .036 * shower_min, 2)
        db.execute("INSERT INTO data(user_id, driving_miles, shower_min, light_hours, food_carbon, total_carbon) VALUES(?,?,?,?,?,?)",
                   user_id, driving_miles, shower_min, light_hours, food_carbon, total_carbon)

    # return logged (page with today's carbon and link to history)
        return render_template("logged.html", carbon=total_carbon, food=food_carbon)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("log.html")


@app.route("/history")
@login_required
def history():
    # show history of carbon emissions

    history = db.execute(
        "SELECT date, total_carbon, food_carbon, shower_min, driving_miles, light_hours FROM data WHERE user_id = ?", session["user_id"])

    x_axis_time = []
    y_axis_carbon = []
    y_axis_food = []
    time = db.execute("SELECT date FROM data WHERE user_id = ?", session["user_id"])
    carbon = db.execute("SELECT total_carbon FROM data WHERE user_id = ?", session["user_id"])

    # if user has not logged any data, redirect to nohistory.html
    if len(carbon) == 0:
        return render_template("nohistory.html")
    else:

        food = db.execute("SELECT food_carbon FROM data WHERE user_id = ?", session["user_id"])

        for i in range(len(carbon)):
            y_axis_carbon.append(carbon[i]["total_carbon"])
            y_axis_food.append(food[i]["food_carbon"])
            # Cut the first two digits of the year from the date so the graph doesn't get crowded
            timecut = str(time[i]["date"])[2:]
            x_axis_time.append(timecut)

        # graph each user's data: total carbon
        plt.plot(x_axis_time,y_axis_carbon,c="#008000", marker=".", ms=14, lw=3)
        plt.title("Check out your progress!")
        plt.xlabel("Date")
        plt.ylabel("Total Carbon Produced (kg)")

        # graph food carbon
        plt.plot(x_axis_time, y_axis_food,c="#261da8", marker=".", ms=14, lw=3)

        plt.legend(['Total Carbon', 'Carbon From Food'])


        # save each user's plot individually
        user = str(session["user_id"])
        filename = "static/plot" + user +".png"
        plt.savefig(filename)
        return render_template("history.html", history=history, filename=filename)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

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


@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    # calculate carbon emissions (theoretical or without account)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Calculate carbon emissions
        driving_miles = int(request.form.get("drive"))
        shower_min = int(request.form.get("shower"))
        light_hours = int(request.form.get("light")) * int(request.form.get("rooms"))

        # calculate carbon from food
        food_carbon = round(6*int(request.form.get("beef")) + 9*int(request.form.get("lamb")) + 2*int(request.form.get("turkey")) + 2*int(
            request.form.get("tuna")) + 2*int(request.form.get("chicken")) + int(request.form.get("cheese")) + 3*int(request.form.get("pork")), 2)

        # calculate the total carbon emissions (all in kg)
        total_carbon = round(food_carbon + .12 * driving_miles + .1 * light_hours + .036 * shower_min, 2)

    # return calculated
        return render_template("calculated.html", carbon=total_carbon, food=food_carbon)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("calculate.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure name was submitted
        if not request.form.get("name"):
            return apology("must provide name", 400)

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 400)

        # Ensure email is valid email address
        # source: https://pypi.org/project/email-validator/
        email = request.form.get("email")
        try:
            # Validate.
            valid = validate_email(email)

            # Update with the normalized form.
            email = valid.email
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
            return apology(str(e), 400)

        # Ensure email is not already in database
        check = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        if len(check) != 0:
            return apology("this email address is already registered.", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Send confirmation email
        msg = Message("You are registered!", recipients=[email])
        msg.html = render_template("register_email.html")
        mail.send(msg)

        # Insert new user into users and hash password
        db.execute("INSERT INTO users (name, email, password) VALUES(?, ?, ?)", request.form.get(
            "name"), email, generate_password_hash(request.form.get("password")))

        return redirect("/login", 200)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
