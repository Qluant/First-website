from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app.models import *

def migrate(db: SQLAlchemy, *models):
    db.drop_all()
    db.create_all()

from app.routes import *
