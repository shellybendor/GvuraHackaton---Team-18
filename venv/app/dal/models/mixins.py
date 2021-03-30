from datetime import datetime

from app import db


class CreatedAtMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
