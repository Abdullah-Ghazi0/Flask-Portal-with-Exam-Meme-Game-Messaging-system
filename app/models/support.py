from ..extensions import db
from datetime import datetime, timezone

class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    catagory = db.Column(db.String, nullable=False)
    reporter_id = db.Column(db.Integer, db.Foreignkey("user.id"), nullable=False)
    target_type = db.Column(db.String, nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String, nullable=False)
