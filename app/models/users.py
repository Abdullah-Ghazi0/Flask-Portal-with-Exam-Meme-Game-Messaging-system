from ..extensions import db
from datetime import datetime, timezone

class  Users(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(50), unique = True, nullable = False)
        email = db.Column(db.String(80), unique=True)
        password = db.Column(db.String(50), nullable = False)
        created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
        status = db.Column(db.String(32), default="active")
        status_changed_at = db.Column(db.DateTime)

        profile = db.relationship('UserProfiles', backref="user", uselist=False)

class UserProfiles(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
        displayname = db.Column(db.String(100), nullable = False)
        bio = db.Column(db.String(256))
        picture = db.Column(db.String(32), default="default.png")
        verified = db.Column(db.Boolean, default=False)
        link = db.Column(db.String(256))