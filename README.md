# Library-Management
Library Management is a simple web application built with Flask that helps librarians manage library books and members. It allows librarians to view and search for books, issue and return books, as well as add new books or import new books to the library.

### [Deployed on render] https://library-management-imsf.onrender.com/

## Features
- Books Management: Allows librarians to add and import books from Frapee API, and update, and delete books from the library's collection.
- Member Management: Enables librarians to manage library members, including adding new members, updating member information, and keeping track of transaction history.
- Transaction Management: All transactions of issuing and returning are recorded.
- Circulation Management: Handles the issuing and returning of books by members. It tracks due dates and manages rent for returns.
- Book Search: Provides a search functionality to find books based on title or author.
- Analytics: Generates graphs for popular books, and top-paying members' data to librarians.
- Colour Modes: The application provides dark and light mode UI.

***
## Installation
- Run the command to cole the repository
```sh
  git clone https://github.com/rajveer-1011/Library-Management.git
```
- Install all requirements with
```sh
cd Library-Management
pip install -r requirements.txt
```
- run command to start the server
```sh
python run.py
```
***
## Technologies Used
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Backend: Flask
- Database: SQLite
- Additional Libraries: Flask-SQLAlchemy (ORM), Chart.js (Analytics), Pdfkit (Export to pdf)

## Screenshots

### Books tab
![Books](/Screen shots/Books page.png)
