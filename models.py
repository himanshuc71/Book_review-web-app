import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book (db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, unique = True, nullable = False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publicationyear = db.Column(db.Integer, nullable=False)
    reviews = db.relationship("Review", backref="book", lazy=True)

    def add_review(self, user_id, text, rating):
        r = Review(user_id = user_id, book_id = self.id, text = text, rating = rating)
        db.session.add(r)
        db.session.commit()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique = True, nullable=False)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    bookid = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)
    text = db.Column(db.String, nullable = True)
    rating = db.Column(db.Integer, nullable = False)
