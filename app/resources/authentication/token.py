from flask import g
from flask_restful import Resource

from app import auth


class APIToken(Resource):
    DEFAULT_TOKEN_DURATION = 600

    decorators = [auth.login_required]

    def get(self):
        token = g.user.generate_auth_token(self.DEFAULT_TOKEN_DURATION)
        return {'token': token, 'duration': self.DEFAULT_TOKEN_DURATION}
