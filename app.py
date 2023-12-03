from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
db = SQLAlchemy(app)
owner = getenv("OWNER")
