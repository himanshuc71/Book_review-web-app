# Book Review
## Book review website using Python, Flask, SQL, and BootStrap where a user can signup, log into and search for books using a name, ISBN or author. Check out reviews and add a review to a book(at most one). Displays ratings and reviews from Goodreads for a broader audience. Uses Goodreads API and Open Library covers API. The website also has its own API.



![](https://github.com/himanshuc71/Book_review/blob/master/demo.jpg)

### API Access: 
If users make a GET request to the website’s /api/<isbn> route, where <isbn> is an ISBN number, the website returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. 
  
### How to run
In the Terminal/cmd prompt,

pip3 install -r requirements.txt

export/set FLASK_APP=application.py

flask run
