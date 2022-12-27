from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, name, email, password, created_on):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.created_on = created_on
    
class Address(db.Model):
    __tablename__ = "adresses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    street_one = db.Column(db.String(200), nullable=False)
    street_two = db.Column(db.String(200))
    city = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    zip = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    landlord_name = db.Column(db.String(200), nullable=False)
    landlord_email = db.Column(db.String(200), nullable=False)
    landlord_phone = db.Column(db.String(200), nullable=False)

    def __init__(self, user_id, street_one, street_two, city, state, zip, start_date, end_date, landlord_name, landlord_email, landlord_phone):
        self.user_id = user_id
        self.street_one = street_one
        self.street_two = street_two
        self.city = city
        self.state = state
        self.zip = zip
        self.start_date = start_date
        self.end_date = end_date
        self.landlord_name = landlord_name
        self.landlord_email = landlord_email
        self.landlord_phone = landlord_phone