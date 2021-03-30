from sqlalchemy import Table, Column, Integer, ForeignKey

from app import db

# represents 'Many-To-Many' relationship between Events and Tags
event_owner_association = Table(
    'event_owners',
    db.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)
