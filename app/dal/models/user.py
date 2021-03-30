from flask_restful import fields
import jwt
import time
from app import db
from app import auth
from flask import current_app, g
from passlib.hash import sha256_crypt
import app.resources.errors as errors
from sqlalchemy.orm import relationship, backref
from app.dal.models.event_participation import EventParticipation
from app.dal.models.story import Story
from app.dal.models.role import Role

JWT_ALGORITHM = 'HS256'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), index=True)
    password_hash = db.Column(db.String(128))
    cellphone = db.Column(db.Unicode(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    roles = relationship(Role, backref='user')

    event_changelog = relationship('Changelog', back_populates='updater')

    participated_events = relationship(EventParticipation, back_populates='participant', cascade="all,delete")
    bravery_stories = relationship(Story, backref='owner')

    def hash_password(self, password):
        self.password_hash = sha256_crypt.encrypt(password)

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password_hash)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm=JWT_ALGORITHM
        )

    def get_roles(self):
        # noinspection PyTypeChecker
        return list(set([role.label for role in self.roles]))

    @staticmethod
    def verify_auth_token(token):
        try:
            token_content = jwt.decode(token,
                                       current_app.config['SECRET_KEY'],
                                       algorithms=[JWT_ALGORITHM]
                                       )
        except jwt.exceptions.ExpiredSignatureError:
            raise errors.APITokenExpired
        except:
            return None  # In case it is an invalid token it can be an email

        return User.query.get(token_content['id'])

    @classmethod
    def marshaller(cls):
        return {
            'id': fields.Integer,
            'email': fields.String,
            'cellphone': fields.String,
            'first_name': fields.String,
            'last_name': fields.String
        }


@auth.verify_password
def verify_password(email_or_token, password):
    user = User.verify_auth_token(email_or_token)
    if not user:
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.get_user_roles
def get_user_roles(user):
    current_user = User.verify_auth_token(user['username'])
    return current_user.get_roles()
