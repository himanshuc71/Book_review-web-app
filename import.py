import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    reader = csv.reader(f, delimiter=',')
    for ISBN, title, author, date in reader:
        book = Book(ISBN_num = ISBN, title = title, author = author, publication_year = date)
        db.session.add(book)
        print(f"Added book with {ISBN}, title : {title}, author: {author}, publication year: {date}.")
    print("commiting")
    db.session.commit()
    print("committed")
if __name__ == "__main__":
    with app.app_context():
        main()
