from dataclasses import dataclass

from flask_restful import fields
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, backref

from app import db
from app.dal.models.tag import Tag
from app.dal.models.user import User
from app.dal.models.media import Media
from app.dal.models.changelog import Changelog
from app.dal.models.event_tags import event_tag_association
from app.dal.models.event_media import event_media_association
from app.dal.models.event_owners import event_owner_association
from app.dal.models.event_participation import EventParticipation
from app.dal.models.mixins import TimestampMixin


class Event(TimestampMixin, db.Model):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    geolocation = Column(String)
    title = Column(String, unique=True)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    reward = Column(Integer)
    participation_secret = Column(String(45))
    participation_secret_qr_url = Column(String)
    tags = relationship(Tag, secondary=event_tag_association)
    changelog = relationship(Changelog, backref=backref('event', cascade="all, delete"))
    media = relationship(Media, secondary=event_media_association, cascade="all, delete")
    owners = relationship(User, secondary=event_owner_association,
                          backref=backref('owned_events', cascade="all, delete"))
    participants = relationship(EventParticipation, back_populates='participated_event', cascade="all, delete")

    @classmethod
    def marshaller(cls):
        return {
            'id': fields.Integer,
            'geolocation': fields.String,
            'title': fields.String,
            'description': fields.String,
            'start_time': fields.DateTime,
            'end_time': fields.DateTime,
            'reward': fields.Integer,
            'tags': fields.List(fields.String),  # TODO: use a Tag.Marshaller instead
            'participants': fields.List(fields.Nested(EventParticipation.marshaller())),
            'status': fields.String(attribute=lambda o: o.changelog[-1].message),
            'media': fields.List(fields.String),
            'owners': fields.List(fields.Nested(User.marshaller()))
        }
