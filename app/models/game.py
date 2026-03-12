from ..extensions import db
# from sqlalchemy.sql import func


class Words(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        word = db.Column(db.String(36), nullable = False)
        k_char = db.Column(db.Integer, nullable = False)