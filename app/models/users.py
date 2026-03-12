from ..extensions import db

class  Users(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(50), unique = True, nullable = False)
        displayname = db.Column(db.String(100), nullable = False)
        password = db.Column(db.String(50), nullable = False)
        picture = db.Column(db.String(32), default="default.png")