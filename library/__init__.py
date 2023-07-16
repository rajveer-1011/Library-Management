from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = "abc"  

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


from library import routes
from library import models

db.init_app(app)

with app.app_context():
    db.create_all()

