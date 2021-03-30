from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, backref

from app import db
from app.dal.models.mixins import CreatedAtMixin
from app.dal.models.user import User


class Changelog(CreatedAtMixin, db.Model):
    __tablename__ = "changelogs"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    updater_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))
    updater = relationship(User, back_populates='event_changelog')
