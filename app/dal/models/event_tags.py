from sqlalchemy import Table, Column, Integer, ForeignKey

from app import db

# represents 'Many-To-Many' relationship between Events and Tags
event_tag_association = Table(
    'event_tags',
    db.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)
