from flask_restful import fields

from sqlalchemy import Integer, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from app import db


class EventParticipation(db.Model):
    __tablename__ = 'event_participation'
    participant_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)
    count = Column(Integer, default=0)
    participant = relationship("User", back_populates="participated_events")
    participated_event = relationship("Event", back_populates="participants")
    validated = Column(Boolean, default=False)

    @classmethod
    def marshaller(cls):
        return {
            'participant': fields.String(attribute=lambda participation: participation.participant.email),
            'validated': fields.Boolean
        }
