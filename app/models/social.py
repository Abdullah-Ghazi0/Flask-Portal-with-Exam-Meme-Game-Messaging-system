from ..extensions import db
from datetime import datetime, timezone

class Follows(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
        followed_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
        created_at = db.Column(db.DateTime(timezone=True), index=True, default=lambda: datetime.now(timezone.utc))

        follower = db.relationship('Users', foreign_keys=[follower_id])
        followed = db.relationship('Users', foreign_keys=[followed_id])

        __table_args__ = (
                db.UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),
                db.Index('idx_follower_followed', 'follower_id', 'followed_id')
        )

        