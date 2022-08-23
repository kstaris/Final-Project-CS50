import os
import sys
from pickle import TRUE
from flask import Flask, redirect, render_template, request, session,jsonify
from flask_session import Session
from cs50 import SQL;
from helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
db = SQL("sqlite:///cars.db")

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MAX_CONTENT_LENGTH"] = 1024
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
#Request that returns all the models of a specified manfacturer
@app.route("/manuf", methods=["POST"])
def manuf():
    if request.method == "POST":
        return jsonify(db.execute("SELECT DISTINCT model FROM allCars WHERE make = ?", request.get_data(as_text=True, cache=False)))
#Request that returns all the manufacturing years of a specified car model
@app.route("/model", methods=["POST"])
def model():
    print("InModel",file=sys.stdout)
    if request.method == "POST":
        return jsonify(db.execute("SELECT DISTINCT year FROM allCars WHERE model = ?", request.get_data(as_text=True)))
#Index page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #Get all the inputs from index page
        manufacturer = request.form.get("manufacturer")
        model = request.form.get("model")
        fConsumption= request.form.get("fConsumption")
        fType= request.form.get("fType")
        fPrice = request.form.get("fPrice")
        kmPy = request.form.get("kmPy")
        tax = request.form.get("tax")
        insurance = request.form.get("insurance")
        oil = request.form.get("oil")
        service = request.form.get("service")
        tyres = request.form.get("tyres")
        parking = request.form.get("parking")
        mPayment = request.form.get("mPayment")
        initPayment = request.form.get("initPayment")
        expSellingPrice = request.form.get("expSellingPrice")
        yearsToHave = request.form.get("yearsToHave")
        reg_year = request.form.get("reg_year")
        mRunCost = request.form.get("mRunCost")
        #Create table if database if a table does not already exist
        db.execute("""CREATE TABLE IF NOT EXISTS saved_cars (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            userId INTEGER NOT NULL, 
            manufacturer TEXT,
            model TEXT,
            reg_year INTEGER,
            fConsumption FLOAT,
            fType TEXT,
            fPrice FLOAT,
            kmPy INTEGER,
            tax FLOAT,
            insurance FLOAT,
            oil FLOAT,
            service FLOAT,
            tyres FLOAT,
            parking FLOAT,
            mPayment FLOAT,
            initPayment FLOAT,
            expSellingPrice FLOAT,
            yearsToHave INTEGER,
            mRunCost FLOAT)""")
        #Insert the newly created car in database
        db.execute("""INSERT INTO saved_cars (userId, manufacturer, model, reg_year, fConsumption, fType, fPrice, kmPy, tax, insurance,
            oil, service, tyres, parking, mPayment, initPayment, expSellingPrice, yearsToHave, mRunCost) VALUES (?)""", (session["user_id"], manufacturer, 
            model, reg_year, fConsumption, fType, fPrice, kmPy, tax, insurance, oil, service, tyres, parking, mPayment, initPayment, expSellingPrice, yearsToHave, mRunCost))
        allManuf = db.execute("SELECT DISTINCT Make FROM allCars")
        return render_template("index.html", allManuf=allManuf)
    else:
        #Renders template with car manudacturers loaded
        allManuf = db.execute("SELECT DISTINCT Make FROM allCars")
        return render_template("index.html", allManuf=allManuf)
#Deletes a car from database
@app.route("/delete", methods =["GET", "POST"])
#Check if user logged in
@login_required
def delete():
    if request.method=="POST":
        #Delete the car
        print(request.form.get('delete'), file=sys.stdout)
        db.execute("DELETE FROM saved_cars WHERE id=?", request.form.get("delete"))
        carsT = db.execute("SELECT * FROM saved_cars WHERE userId = ?", session["user_id"])
        return render_template("saved.html", carsT=carsT)

@app.route("/saved", methods =["GET", "POST"])
@login_required
def saved():
    if request.method == "POST":
        carsT = db.execute("SELECT * FROM saved_cars WHERE userId = ?", session["user_id"])
        car1=0
        car2=0
        car3=0
        i=0
        #Get cars to compare
        carIds = request.form.getlist("car_checkbox")
        for carId in carIds:
            if car1 == 0:
                car1 = carId
            elif car2 == 0:
                car2 = carId
            elif car3 ==0:
                car3 = carId
            else:
                #Render error
                return render_template("saved.html", carsT=carsT, max3="Maximum 3 cars can be compared")
        #Render car comparison table
        carCompTable = db.execute("SELECT * FROM saved_cars WHERE id = ? OR id = ? OR id = ?", car1, car2, car3)
        return render_template("saved.html", carCompTable = carCompTable, carsT = carsT)
    else:
        #Rander all user cars table
        carsT = db.execute("SELECT * FROM saved_cars WHERE userId = ?", session["user_id"])
        return render_template("saved.html", carsT = carsT)
        

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method=="POST":
        #Render edit template
        eTable= db.execute("SELECT * FROM saved_cars WHERE id = ?", request.form.get("edit"))
        allManuf = db.execute("SELECT DISTINCT Make FROM allCars")
        return render_template("edit.html", eTable=eTable, allManuf=allManuf)

@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method=="POST":
        manufacturer = request.form.get("manufacturer")
        model = request.form.get("model")
        fConsumption= request.form.get("fConsumption")
        fType= request.form.get("fType")
        fPrice = request.form.get("fPrice")
        kmPy = request.form.get("kmPy")
        tax = request.form.get("tax")
        insurance = request.form.get("insurance")
        oil = request.form.get("oil")
        service = request.form.get("service")
        tyres = request.form.get("tyres")
        parking = request.form.get("parking")
        mPayment = request.form.get("mPayment")
        initPayment = request.form.get("initPayment")
        expSellingPrice = request.form.get("expSellingPrice")
        yearsToHave = request.form.get("yearsToHave")
        reg_year = request.form.get("reg_year")
        mRunCost = request.form.get("mRunCost")
        #Update car with inserted parameters
        db.execute("""UPDATE saved_cars SET manufacturer = ?, 
        model = ?, reg_year = ?, fConsumption = ?, fType = ?, 
        fPrice = ?, kmPy = ?, tax = ?, insurance = ?, 
        oil = ?, service = ?, tyres = ?, parking = ?, 
        mPayment = ?, initPayment = ?, expSellingPrice = ?, 
        yearsToHave = ?, mRunCost = ? WHERE id = ?""", manufacturer, model, reg_year, fConsumption, fType, fPrice, kmPy, tax, insurance, oil, service, tyres, parking, mPayment, initPayment, expSellingPrice, yearsToHave, mRunCost, request.form.get('id'))
        return redirect("/saved")

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
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure passwords match
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords did not match", 400)
        elif db.execute("SELECT username FROM users WHERE username = (?)", (request.form.get("username"))):
            return apology("Username already exists", 400)
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (?)", (request.form.get("username"), generate_password_hash(request.form.get("password"))))
            rows = db.execute("SELECT * FROM users WHERE username = (?)", (request.form.get("username")))
            session["user_id"] = rows[0]["id"]
            print (session["user_id"], file=sys.stdout)
            return redirect("/")        
    else:
        return render_template("register.html")
        
@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if not request.form.get("password"):
            return apology("must provide password", 403)
        elif request.form.get("password") != request.form.get("password_again"):
            return apology("passwords did not match", 403)
        elif not check_password_hash(rows[0]["hash"], request.form.get("password_existing")):
            return apology("Invalid password")
        else:
            db.execute("UPDATE users SET hash=(?) WHERE id=(?)", generate_password_hash(
                request.form.get("password")), session["user_id"])
            return redirect("/")
    else:
        return render_template("changePassword.html")
