from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class  Users(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(50), unique = True, nullable = False)
        password = db.Column(db.String(50), nullable = False)

class Questions(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        q_text = db.Column(db.String(256), nullable = False)
        answer = db.Column(db.Boolean, nullable = False)

class Results(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        score = db.Column(db.Integer, nullable = False)
    

