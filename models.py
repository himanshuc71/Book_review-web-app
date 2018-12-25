import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book (db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    ISBN_num = db.Column(db.String, unique = True, nullable = False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.String, nullable=False)
