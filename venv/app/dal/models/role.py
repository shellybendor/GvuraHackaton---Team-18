from app import db
from sqlalchemy import Column, Integer, ForeignKey, String


class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    label = Column(String(20))
