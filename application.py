import os, requests
from flask import Flask, session, render_template, jsonify, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#Goodreads API Key
BOOKREAD_API_KEY = "vblp6JmsLMf9SehrZSbqQ"
#postgres url
DATABASE_URL = "postgres://qdzyngedqxnukc:884b4093dc638c2b0a6108356bbcf1d6bcfb839923e048bb7220649cbc254453@ec2-107-20-237-78.compute-1.amazonaws.com:5432/d3nnekv2913b3f"


app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = :username and password = :password",
        {"username": username, "password": password} ).fetchone()
        #check if user exist in the database
        if user is None or username is None or password is None:
            return render_template("error.html", message = "username and password does not match")
        else:
            #log the user in
            session["user_id"] = user.username
            return render_template("search.html", username = username)
    #if user has not logged out
    elif session.get("user_id") is not None:
        return render_template("search.html", username = session.get("user_id"))
    # GET request
    else:
        return render_template("index.html")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        f = request.form.get("fname")
        l = request.form.get("lname")
        u = request.form.get("username")
        p = request.form.get("password")
        cp = request.form.get("confirmpassword")
        e = request.form.get("email")
        # if a field is left empty by the user(tested)
        if u is "" or p is "" or e is "" or cp is "" or f is "" or l is "":
            return render_template("signup.html", message = "Please fill all fields to sign up")
        # if passwords don't match(tested)
        if p != cp:
            return render_template("signup.html", message = "Passwords don't match")
        # if username already exists in database(tested)
        if db.execute("SELECT username FROM users WHERE username = :username",
            {"username": u}).rowcount > 0:
            return render_template("signup.html", message = "Username already exists")
        # unique email check(tested)
        if db.execute("SELECT email FROM users WHERE email = :email",
            {"email": e}).rowcount > 0:
            return render_template("signup.html", message = "Email already exists please use another email")
        # register user into database(tested)
        else:
            db.execute("INSERT into users(username, password, email, fname, lname) VALUES (:username,:password,:email,:fname,:lname)",
            {"username": u, "password": p,"email": e, "fname": f, "lname": l})
            db.commit()
            return render_template("signup.html", text = "Registeration successfully!")

    # Get Request
    return render_template("signup.html")

# logout feature
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return render_template("index.html")

# Search page functionality
@app.route("/search", methods=['GET','POST'])
def search():
    if session.get("user_id") is None:
        render_template("error.html", message = "Login Required")
    if request.method == 'POST':
        # user is searching by title
        if request.form.get("inlineRadioOptions") == "option1":
            user_search = request.form.get("search")
            book_search = db.execute("SELECT * FROM books WHERE title LIKE LOWER(:s)", { "s": '%' + user_search + '%'}).fetchall()
            return render_template("search.html", username = session["user_id"], result = book_search)
        # user is searching by ISBN
        elif request.form.get("inlineRadioOptions") == "option2":
            user_search = request.form.get("search")
            book_search = db.execute("SELECT * FROM books WHERE isbn LIKE LOWER(:s)", { "s": '%' + user_search + '%'}).fetchall()
            return render_template("search.html", username = session["user_id"], result = book_search)
        # user is searching by author name
        else:
            user_search = request.form.get("search")
            book_search = db.execute("SELECT * FROM books WHERE author LIKE LOWER(:s)", { "s": '%' + user_search + '%'}).fetchall()
            return render_template("search.html", username = session["user_id"], result = book_search)
    return render_template("search.html", username = session["user_id"])

############################################## finish this and the radio check problem
@app.route("/book", methods=['GET','POST'])
def book():
    return render_template("book.html")

# api design that returns a json object
@app.route("/api/<string:isbn>")
def api(isbn):
    if db.execute('SELECT * FROM books WHERE isbn = :isbn', {"isbn": isbn}).rowcount == 0:
        return jsonify({"error":"Invalid ISBN"}), 404

    jsonobj = {"title": "",
                "author": "",
                "year": 0,
                "isbn": isbn,
                "review_count": 0,
                "average_score": 0.0}
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": BOOKREAD_API_KEY, "isbns": isbn})

    jsonobj["average_score"] = res.json()['books'][0]['average_rating']
    jsonobj["review_count"] = res.json()['books'][0]['work_ratings_count']

    data = db.execute("SELECT title, author, publicationyear FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    jsonobj["title"] = data.title
    jsonobj["author"] = data.author
    jsonobj["year"] = data.publicationyear


    return jsonify(jsonobj)
