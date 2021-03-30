import enum
from dataclasses import dataclass
from flask_restful import fields
from app import db
from sqlalchemy import Column, String, Integer, Enum


class TagRelevance(enum.Enum):
    Events = 1
    Stories = 2


class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    label = Column(String, unique=True)
    relevance = Column(Enum(TagRelevance))

    # TODO: find a way to properly use a marshaller to do so
    def __repr__(self):
        return self.label
