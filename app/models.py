from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime, timezone

db = SQLAlchemy()

class  Users(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(50), unique = True, nullable = False)
        displayname = db.Column(db.String(100), nullable = False)
        password = db.Column(db.String(50), nullable = False)
        picture = db.Column(db.String(32), default="default.png")

class Questions(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        q_text = db.Column(db.String(256), nullable = False)
        answer = db.Column(db.Boolean, nullable = False)

class Results(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        score = db.Column(db.Integer, nullable = False)
    
class Words(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        word = db.Column(db.String(36), nullable = False)
        k_char = db.Column(db.Integer, nullable = False)

class Messages(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        s_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        r_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        content = db.Column(db.String(500), nullable = False)
        time = db.Column(db.DateTime(timezone=True), index=True, default=lambda: datetime.now(timezone.utc))

        sender = db.relationship('Users', foreign_keys=[s_id])
        reciever = db.relationship('Users', foreign_keys=[r_id])