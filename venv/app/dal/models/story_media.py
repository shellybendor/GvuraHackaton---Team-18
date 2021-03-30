from sqlalchemy import Table, Column, Integer, ForeignKey

from app import db

# represents 'Many-To-Many' relationship between Story and Media
story_media_association = Table(
    'story_media',
    db.metadata,
    Column('story_id', Integer, ForeignKey('bravery_stories.id')),
    Column('media_id', Integer, ForeignKey('media.id'))
)
