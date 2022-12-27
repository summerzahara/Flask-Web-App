from flask import Flask, render_template, request, session, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from models import db, User, Address


app = Flask(__name__)
app.secret_key = "your_mom"
app.debug = True

# Config Database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost/flaskdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()



@app.route("/")
def index():
    if "user" in session:
        user = session["user"]
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user = session["user"]
        user_id = (User.query.filter(User.username == user).first()).id

        # Query for all address entries
        results = Address.query.filter(Address.user_id == user_id).all()
        return render_template("dashboard.html", user=user, results=results)
    return redirect("/login")

@app.route("/about")
def about():
    if "user" in session:
        user = session["user"]
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check required fields entered
        if not request.form.get("username"):
            flash("You must enter your username", "error")
            return render_template("login.html")
        if not request.form.get("password"):
            flash("You must enter your password", "error")
            return render_template("login.html")
        # Store input as variable
        username = request.form.get("username")
        password = request.form.get("password")

        # Check for user in database
        validate_user = User.query.filter(User.username == username)
        if validate_user is None:
            flash("Invalid username", "error")
            return render_template("login.html")

        # Validate password
        # SELECT password FROM users WHERE username=username
        hashed_pass = (User.query.filter(User.username == username).first()).password
        validate_password = check_password_hash(hashed_pass[0], password)
        if validate_password is None:
            flash("Invalid password", "error")
            return render_template("login.html")

        else:
            # Store user in session
            session["user"] = request.form.get("username")
            return redirect("/dashboard")
    else:
        if "user" in session:
            user = session["user"]
            return redirect("/dashboard")
        else:
            return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Store info as variables
        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("password")
        password2 = request.form.get("password-confirm")

        # check is username is unique
        results = User.query.all()
        for result in results:
            if result.username == username:
                flash("Username already exists", "error")
                return render_template("register.html")
        # check all fields are populated
        if username == "" or name == "" or email == "" or password1 == "" or password2 == "":
            flash("You must populate all fields", "error")
        # Check passwords match
        elif password1 != password2:
            flash("Your passwords do not match", "error")
            return render_template("register.html")
        else:
            # Hash password
            password = generate_password_hash(password1)
            # Store date in variable
            created_on = datetime.datetime.now()
            try:
                # Add user to datable
                new_user = User(username, name, email, password, created_on)
                db.session.add(new_user)
                db.session.commit()
                flash("You are registered!")
                session["user"] = request.form["username"]
                return redirect("/dashboard")
            except:
                flash("Registration Error","error")
                return render_template("register.html")

    else:
        return render_template("register.html")

@app.route("/addaddress", methods=["GET", "POST"])
def addaddress():
    if request.method == "POST":
        # Store Input as variables
        user = session["user"]
        street_one = request.form.get("street1")
        street_two = request.form.get("street2")
        city = request.form.get("city")
        state = request.form.get("state")
        zip = request.form.get("zip")
        landlord_name = request.form.get("landlord-name")
        landlord_email = request.form.get("landlord-email")
        landlord_phone = request.form.get("landlord-phone")
        start_date = request.form.get("startdate")
        end_date = request.form.get("enddate")
        
        # Check for required fields
        if street_one == "" or city == "" or state == "" or zip == "" or landlord_name == "" or landlord_email == "" or landlord_phone == "" or start_date == "" or end_date == "":
            flash("Please populate required fields", category="error")
            return render_template("addaddress.html")
        # Find user_id in database
        user_id = (User.query.filter(User.username == user).first()).id
        print(user_id)
        # Add address to database
        try:
            new_address = Address(user_id, street_one, street_two, city, state, zip, start_date, end_date, landlord_name, landlord_email, landlord_phone)
            print(new_address.user_id, new_address.street_one, new_address.street_two, new_address.city, new_address.state, new_address.landlord_name, new_address.landlord_email, new_address.landlord_phone, new_address.start_date, new_address.end_date)
            db.session.add(new_address)
            db.session.commit()
            flash("Address added!", "success")
            return redirect("/dashboard")
        except:
            flash("Error adding address", "error")
            return render_template("addaddress.html")
    else:
        if "user" in session:
            user = session["user"]
            return render_template("addaddress.html")
        else:
            return redirect("/login")



if __name__ == "__main__":
    app.run()
