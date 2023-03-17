from app import db

# "Achievement" table should be in relationships with "User". If I have time I will do it.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    language = db.Column(db.String(2), default="en")
    register_date = db.Column(db.String(40), nullable=False)
    bonus_taked = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(20), default="Newbie")
    coins = db.Column(db.Integer, default=0)


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
