from sqlalchemy import Table, Column, Integer, ForeignKey

from app import db

# represents 'Many-To-Many' relationship between Events and Media
event_media_association = Table(
    'event_media',
    db.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('media_id', Integer, ForeignKey('media.id'))
)
