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
***
### Home page
![Home](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Homepage.png)
***
### Books Tab
![Books](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Books%20page.png)
#### Add Book
![Add Book](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Add%20book%20page.png)
#### Edit Book
![Edit Book](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Update%20book%20page.png)
#### Delete Book
![Delete Book](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Delete%20book.png)
#### Book Details
![Book details](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Book%20details.png)
#### Import book from Frapee API
![Import book from Frapee API](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Import%20book.png)
***
### Members Tab
#### Add Member
![Add Member](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Members%20page.png)
#### Edit Member
![Edit Member](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Update%20member%20page.png)
#### Delete Member
![Delete Member](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Delete%20user.png)
#### Member's transaction
![Member's transaction](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/member%20transaction%20page.png)
***
### Transactions
#### Transactions table
![Transactions table](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Transaction%20page.png)
#### Export transactions
![Export transactions](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/export%20page.png)
***
### Analytics Tab
#### Graphs
![Graphs](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Analytics%20page.png)
***
### Not returned books
![Not returned books](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/not%20return%20transaction.png)
***
### Issue book
![Issue book](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Issue%20book.png)
***
### Return book
![Return book](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/Return%20book.png)
***
### Search tab
#### Search result
![Search result](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/search%20page.png)
***
### Theme mode
#### Dark mode
![Dark mode](https://github.com/rajveer-1011/Library-Management/blob/main/Screen%20shots/dark%20mode.png)

  


