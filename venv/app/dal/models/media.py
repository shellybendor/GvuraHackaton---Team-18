import enum

from app import db
from sqlalchemy import Column, Integer, Enum, String


class MediaType(enum.Enum):
    Image = 1
    Video = 2
    Sound = 3


class Media(db.Model):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(MediaType))
    url = Column(String)

    def __repr__(self):
        return self.url  # TODO: make marshall instead of this
