import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book (db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key = True)
    ISBN_num = db.Column(db.String, unique = True, nullable = False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    reviews = db.relationship("Review", backref="book", lazy=True)

    def add_review(self, user_id, text, rating):
        r = Review(user_id = user_id, book_id = self.id, text = text, rating = rating)
        db.session.add(r)
        db.session.commit()

class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique = True, nullable=False)

class Review(db.Model):
    __tablename__ = "Reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("Books.id"), nullable = False)
    text = db.Column(db.String, nullable = True)
    rating = db.Column(db.Integer, nullable = False)
    db.CheckConstraint("rating>0 AND rating<6 ")
