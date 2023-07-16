from library import db


class Users(db.Model):
    userID=db.Column(db.Integer, primary_key=True)
    userName=db.Column(db.String, nullable=False, unique=True) 
    name = db.Column(db.String(), nullable=False)
    userEmail=db.Column(db.String, nullable=False,unique = True) 
    debt = db.Column(db.Integer, default=0)
    total_paid = db.Column(db.Integer(), default = 0)

class Books(db.Model):
    bookID = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(), nullable=False)
    authors = db.Column(db.String(), nullable=False)
    average_rating = db.Column(db.Float(), nullable=False)
    isbn = db.Column(db.Integer(), nullable=False)
    isbn13 = db.Column(db.Integer(), nullable=False)
    language_code = db.Column(db.String(), nullable=False)
    num_pages = db.Column(db.Integer(), nullable=False)
    ratings_count =db.Column(db.Integer(), nullable=False)
    text_reviews_count = db.Column(db.Integer(), nullable=False)
    publication_date =db.Column(db.String(), nullable=False)
    publisher = db.Column(db.String(), nullable=False)
    member_count = db.Column(db.Integer(), default = 0)
    quantity = db.Column(db.Integer(), nullable=False)
    rent = db.Column(db.Integer(), nullable=False)
  

class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_ID = db.Column(db.Integer(), db.ForeignKey('users.userID'))
    book_ID = db.Column(db.Integer(), db.ForeignKey('books.bookID'))
    IssueDate = db.Column(db.DateTime, nullable=False)
    ExpRetDate = db.Column(db.Date, nullable=False, default=None)
    ActRetDate = db.Column(db.DateTime, default=None)
    status = db.Column(db.String, nullable=False, default="issued")
    user = db.relationship('Users')
    book = db.relationship('Books')
