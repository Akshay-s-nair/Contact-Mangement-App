# models.py

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    profile_picture = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(70), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    contacts = db.relationship('Contacts', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.firstname}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    company = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(15), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'address': self.address,
            'company': self.company,
            'phone': self.phone
        }


class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __repr__(self):
        return f"<TokenBlacklist {self.token}>"
