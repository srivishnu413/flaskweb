# import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Create our instantiator flask
app = Flask(__name__)

# DB Configuration
# Local Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskaws' # 'mysql://username:password@server/db'
# AWS Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://admin:Srikanth1977@flaskdb.cipcosbd1ddo.us-east-1.rds.amazonaws.com/flaskaws' # 'mysql://username:password@server/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"

# Add Database Configuration to Flask
db = SQLAlchemy(app)

# Create a Table/Model in our Database
# Models are classes that we can use and that extends from db.Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)


# Init Method
def __init__(self,title,author,price):
    self.title = title
    self.author = author
    self.price = price



# Create a Route
@app.route('/')
# Create a View function
def index():
    # Query the Book Table = Get all the books from the database
    books = Book.query.all()
    # To show index.html we use render_template from Flask
    return render_template('index.html', books=books) # we can access the books inside the index.html

# Method to add a Book
@app.route('/add/', methods=['POST'])
def insert_book():
    if request.method == "POST":
        book = Book(
            title = request.form.get('title'),
            author = request.form.get('author'),
            price = request.form.get('price')
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully")
        return redirect(url_for('index'))

# Update Route
@app.route('/update/', methods=["POST"])
def update():
    if request.method == "POST":
        my_data = Book.query.get(request.form.get('id'))
        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.price = request.form['price']

        db.session.commit()
        flash("Book updated successfully")
        return redirect(url_for('index'))


# Delete Route
@app.route('/delete/<id>/', methods=["GET", "POST"])
def delete(id):
    my_data = Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book deleted successfully")
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=True) # In Development Mode : debug = True, In production mode you can remove it.
