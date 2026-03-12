from ..extensions import db
from datetime import datetime, timezone

class Messages(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        s_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        r_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        content = db.Column(db.String(500), nullable = False)
        time = db.Column(db.DateTime(timezone=True), index=True, default=lambda: datetime.now(timezone.utc))
        read = db.Column(db.Boolean, default=False)

        sender = db.relationship('Users', foreign_keys=[s_id])
        reciever = db.relationship('Users', foreign_keys=[r_id])