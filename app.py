from flask import Flask, jsonify, request
from flask_cors import CORS 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///final-project.db"
db.init_app(app)
CORS(app)
Migrate(app, db)

    






app.run(host="localhost", port=8080)