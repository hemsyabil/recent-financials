from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app import finance_app

db = SQLAlchemy(finance_app)
bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode(
            'utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
