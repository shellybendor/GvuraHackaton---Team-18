from flask_restful import fields
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.dal.models.media import Media
from app.dal.models.mixins import TimestampMixin
from app.dal.models.story_media import story_media_association
from app.dal.models.story_tags import story_tag_association
from app.dal.models.tag import Tag


class Story(TimestampMixin, db.Model):
    __tablename__ = "bravery_stories"

    id = Column(Integer, primary_key=True)
    title = Column(String(45), unique=True)
    description = Column(String)
    text = Column(String)
    approved = Column(Integer)
    date = Column(DateTime)
    country = Column(String(100))
    tags = relationship(Tag, secondary=story_tag_association)
    media = relationship(Media, secondary=story_media_association)
    owner_id = Column(Integer, ForeignKey('users.id'))

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    @classmethod
    def marshaller(cls):
        return {
            'id': fields.Integer,
            'title': fields.String,
            'description': fields.String,
            'text': fields.String,
            'date': fields.DateTime,
            'country': fields.String,
            'tags': fields.List(fields.String),  # TODO: use a Tag.Marshaller instead
            'media': fields.List(fields.String),  # TODO: use a Media.Marshaller instead
        }
