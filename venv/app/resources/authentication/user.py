from http import HTTPStatus
from app import db
from flask_restful import Resource, marshal_with
import app.dal.models as models
from app.resources.authentication.authentication_utils import user_creation_parser
import app.resources.errors as errors


class User(Resource):
    MINIMUM_PASSWORD_LENGTH = 10

    @marshal_with(models.User.marshaller())
    def get(self, user_id):
        user = models.User.query.get(user_id)
        if not user:
            raise errors.NoSuchUser
        return user, HTTPStatus.OK

    @marshal_with(models.User.marshaller())
    def post(self):
        args = user_creation_parser.parse_args()
        email = args.get('email')
        password = args.get('password')
        cellphone = args.get('cellphone')
        first_name = args.get('first_name')
        last_name = args.get('last_name')

        if len(password) < self.MINIMUM_PASSWORD_LENGTH:
            raise errors.PasswordIsTooShort
        if models.User.query.filter_by(email=email).first() is not None:
            raise errors.EmailAlreadyTaken

        user = models.User(email=email)
        user.hash_password(password)

        user.cellphone = cellphone
        user.first_name = first_name
        user.last_name = last_name

        try:
            db.session.add(user)
            db.session.commit()
            return user, HTTPStatus.CREATED

        except:
            db.session.rollback()
            raise errors.InternalServerError
