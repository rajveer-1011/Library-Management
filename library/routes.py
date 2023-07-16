from library import app, db
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, make_response
from library.models import Books, Users, Transaction
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
import pdfkit


import json
import requests

# Home page Routes
@app.route("/")
def home():
    book = db.session.query(Books).count()
    user = db.session.query(Users).count()
    issued = db.session.query(Transaction).filter_by(status="issued").count()
    returned =  db.session.query(Transaction).filter_by(status="returned").count()
    notReturned = Transaction.query.filter((Transaction.ExpRetDate < datetime.utcnow())  & (Transaction.status == "issued") ).count()
    users = Users.query.order_by(Users.userName).all()
    books =  Books.query.order_by(Books.title).all()
    book_stock = db.session.query(Books).filter(Books.quantity).all()
    date = datetime.utcnow().date()
    return render_template('homePage.html', users=users, books=books , user=user, issued=issued, returned=returned,  book=book, book_stock=book_stock , date=date , notReturned=notReturned)

# All Books Routes
@app.route("/books")
def books():
    books = Books.query.order_by(Books.title).all()
    users = Users.query.order_by(Users.userName).all()
    date = datetime.utcnow().date()
    return render_template('Books/booksPage.html', books=books, users=users, date=date)


@app.route("/book/<int:id>")
def book(id):
    query = Books.query.get(id)
    return render_template('Books/bookDetailsPage.html', query=query)


@app.route("/add/book", methods=["GET", "POST"])
def book_create():
    if request.method == "POST":
        book = Books(
            title=request.form["title"],
            authors=request.form["authors"],
            average_rating=request.form["average_rating"],
            isbn=request.form["isbn"],
            isbn13=request.form["isbn13"],
            language_code=request.form["language_code"],
            num_pages=request.form["num_pages"],
            ratings_count=request.form["ratings_count"],
            text_reviews_count=request.form["text_reviews_count"],
            publication_date=request.form["publication_date"],
            publisher=request.form["publisher"],
            quantity=request.form["quantity"],
            rent=request.form["rent"],
        )
        db.session.add(book)
        db.session.commit()

        flash("Book created sucessfully", category='success')

        return redirect(url_for("books"))
    return render_template("Books/addBookPage.html")


@app.route("/update/book/<int:id>", methods=["GET", "POST"])
def update_book(id):
    book = db.get_or_404(Books, id)
    if request.method == "POST":
        book.title = request.form["title"]
        book.authors = request.form["authors"]
        book.average_rating = request.form["average_rating"]
        book.isbn = request.form["isbn"]
        book.isbn13 = request.form["isbn13"]
        book.language_code = request.form["language_code"]
        book.num_pages = request.form["num_pages"]
        book.ratings_count = request.form["ratings_count"]
        book.text_reviews_count = request.form["text_reviews_count"]
        book.publication_date = request.form["publication_date"]
        book.publisher = request.form["publisher"]
        book.quantity = request.form["quantity"]
        book.rent = request.form["rent"]
        db.session.commit()
        flash("Book updated sucessfully", category='success')
        return redirect(url_for("books"))
    return render_template("Books/updateBookPage.html", book=book)


@app.route("/delete/book/<int:id>", methods=["GET", "POST"])
def delete_book(id):
    book = db.get_or_404(Books, id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted sucessfully", category='success')
    return redirect(url_for("books"))


@app.route("/issuebook", methods=['GET', 'POST'])
def issuebook():
    if request.method == "POST":
        user = Users.query.get(request.form["userId"])
        book = Books.query.get(request.form["bookId"])
        # check for book availability
        if (book.quantity == 0):
            flash("Book Out of Stock", category='danger')
            return redirect(url_for("index"))
        elif ((user.debt+book.rent) <= 500):
            issue = Transaction(
                user_ID=request.form["userId"],
                book_ID=request.form["bookId"],
                IssueDate=datetime.utcnow(),
                ExpRetDate=datetime.strptime(request.form["ExpRetDate"],'%Y-%m-%d'),
            )
            db.session.add(issue)
            db.session.commit()

            query = Books.query.get(request.form["bookId"])
            # stock quantity decreased
            query.quantity = query.quantity-1
            query.member_count = query.member_count+1
            db.session.commit()
            flash(f"{query.title} successfully issued to {user.name}", category='success')
            return redirect(url_for("transaction"))
        else:
            flash("User Debt limit exceeded more than 500", category='danger')
            return redirect(url_for("home"))


@app.route("/returnbook", methods=['GET', 'POST'])
def returnbook():
    if request.method == "POST":
        if request.form["return"] == "returnBook":
            transactionId = int(request.form["id"])
            trans = db.get_or_404(Transaction, transactionId)
            if (trans.status == "issued"):
                ActRetDate = datetime.utcnow()
                trans.ActRetDate = ActRetDate
                trans.status = "returned"
                query = Books.query.get(trans.book_ID)
                query.quantity = query.quantity+1
                user = Users.query.get(trans.user_ID)
                paid = request.form["paid"]
                # if paid is checked 
                if (paid == "yes"):
                    user.total_paid = user.total_paid + query.rent
                # if paid not checked amount added to debt
                else:
                    user.debt = user.debt + query.rent
                db.session.commit()
                flash("Book returned sucessfully", category='success')
            else:
                flash("Book is returned already", category='danger')
            return redirect(url_for("home"))

        if request.form["return"] == "returnBookInfo":
            userID = int(request.form["userId"])
            user = Users.query.get(userID)
            query1 = Transaction.query.filter((Transaction.user_ID==userID) & (Transaction.status=="issued")).all()
            return render_template("Books/returnbookPage.html", query1=query1,user=user)

# All Members Routes
@app.route("/members")
def members():
    query = Users.query.all()
    return render_template('Members/membersPage.html', query=query)


@app.route("/add/member", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        try:
            member = Users(
                userName=request.form["username"],
                name=request.form["name"],
                userEmail=request.form["userEmail"],
            )
            db.session.add(member)
            db.session.commit()
            flash("Member created successfully", category='success')
            return redirect(url_for("members"))
        # if integrity error occurs
        except IntegrityError:
                    db.session.rollback()
                    flash(f"This username or email already exists!", category="danger")
                    return redirect(url_for("add_member"))
        
    return render_template("Members/addMemberPage.html")


@app.route("/delete/member/<int:id>")
def delete_member(id):
    member = db.get_or_404(Users, id)
    db.session.delete(member)
    db.session.commit()
    return redirect(url_for("members"))


@app.route("/update/member/<int:id>", methods=['GET', 'POST'])
def update_member(id):
    member = db.get_or_404(Users, id)
    if request.method == "POST":
        member.userName = request.form['userName']
        member.userEmail = request.form['userEmail']
        member.phoneNo = request.form['phoneNo']
        db.session.commit()
        flash("Member updated successfully", category='success')
        return redirect(url_for("members"))
    return render_template("Members/updateMemberPage.html", member=member)

# All Transaction Routes
@app.route("/transaction")
def transaction():
    query = Transaction.query.all()
    return render_template('Transactions/transactionPage.html', query=query, name="Transactions")


@app.route("/transaction/notreturn")
def transaction_notreturn():
    query =  Transaction.query.filter((Transaction.ExpRetDate < datetime.utcnow())  & (Transaction.status == "issued") ).all()
    return render_template('Transactions/transactionPage.html', query=query, name = "Not return transactions")


@app.route("/transaction/member/<int:id>")
def member_transaction(id):
    user = db.get_or_404(Users, id)
    query = Transaction.query.filter((Transaction.user_ID==id)).all()
    return render_template('Transactions/memberTransaction.html', query=query, user=user)


@app.route('/search', methods=['GET', 'POST'])
def search():
    books = Books.query
    searchbox = request.form['searched']
    # search query
    squery = books.filter(Books.title.like('%' + searchbox + '%')
                          | Books.authors.like('%' + searchbox + '%'))
    squery = squery.order_by(Books.title).all()
    return render_template('Books/searchResultPage.html', squery=squery, search=searchbox)


@app.route('/importBooks', methods=['GET', 'POST'])
def importBooks():
    books = []
    nbooks = request.form['nbooks']
    nbooks = int(nbooks) if (nbooks != "") else 20
    title = request.form['title']
    response = requests.get(f"https://frappe.io/api/method/frappe-library?title={title}") if (title != "") else requests.get(f"https://frappe.io/api/method/frappe-library")
    books = response.json()['message']
    book_list = db.session.query(Books.title).all()
    book_list = list(map(' '.join, book_list))
    author_list = db.session.query(Books.authors).all()
    author_list = list(map(' '.join, author_list))
    count = 0
    # if books are succesfully imported
    if len(books) > 0:
        for index, book in enumerate(books):            
            if index == (nbooks): 
                print ("break") # if books of n no. is imported 
                break
            try:
                # if no duplicate book is found
                if(book['bookID'] not in book_list and book['authors'] not in author_list):
                    book_to_create = Books(
                                    bookID = book['bookID'],
                                    title = book['title'], 
                                    authors = book['authors'],
                                    average_rating = book["average_rating"],
                                    isbn = book["isbn"],
                                    isbn13 = book["isbn13"],
                                    language_code = book["language_code"],
                                    num_pages = book["  num_pages"],
                                    ratings_count = book["ratings_count"],
                                    text_reviews_count = book["text_reviews_count"],
                                    publication_date = book["publication_date"],
                                    publisher = book["publisher"],
                                    quantity = 20,
                                    rent = 150)
                    db.session.add(book_to_create)
                    db.session.commit()
                    count = count+1
            except IntegrityError:
                    db.session.rollback()
                    flash(f"This book with bookId already exists!", category="danger")
            else:
                continue
        # index calculation
        index = int(nbooks) if (nbooks != "") else index+1
        if count == 0:
            flash(f"Got {index} books from API & All {index} books are already present in database.", category="warning")
        else:
            flash(f"Got {index} books from API succesfully Imported {count} books.", category="success")
    # if error in importing the books
    else:
        flash("No response from the API", category="danger")

    return redirect(url_for('books'))


@app.route('/graphs', methods = ['GET','POST']) 
def graphs():
    books = Books.query.all()
    members = Users.query.all()
    popular_books_title = []
    books_count = []
    member_paying_most = []
    member_paid = []
    # reads top 10 books in descending order
    popular_books = Books.query.order_by(desc(Books.member_count)).limit(10).all()
    # reads top highest paying customers
    most_paying_members = Users.query.order_by(desc(Users.total_paid)).limit(10).all()
    for book in popular_books:
        if book.member_count > 0:
            popular_books_title.append(book.title[0:20])
            books_count.append(book.member_count)

    popular_books_title = json.dumps(popular_books_title)
    books_count = json.dumps(books_count)

    for member in most_paying_members:
        if member.total_paid > 0:
            member_paying_most.append(member.userName)
            member_paid.append(member.total_paid)

    member_paying_most = json.dumps((member_paying_most))
    member_paid = json.dumps((member_paid))

    return render_template("analyticsPage.html",members = len(members), 
                            books = len(books), member_paid = member_paid, 
                            book_title = popular_books_title, 
                            members_name = member_paying_most, 
                            book_count = books_count)


@app.route('/export')
def export():
    query = Transaction.query.all()
    html = render_template('Transactions/exportpdf.html', query=query)
    pdf = pdfkit.from_string(html,False)
    response = make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=transaction_exported.pdf'
    return response

   
   






