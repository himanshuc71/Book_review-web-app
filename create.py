import os

from flask import Flask, render_template, request
from models import *
from application import DATABASE_URL

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# creates all the tables from models.py
def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
