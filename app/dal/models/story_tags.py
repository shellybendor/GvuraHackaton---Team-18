from sqlalchemy import Table, Column, Integer, ForeignKey

from app import db

# represents 'Many-To-Many' relationship between Stories and Tags
story_tag_association = Table(
    'story_tags',
    db.metadata,
    Column('story_id', Integer, ForeignKey('bravery_stories.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)
