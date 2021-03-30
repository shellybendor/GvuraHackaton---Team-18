from flask_restful import reqparse
from validators import email


def email_type(some_str):
    if email(some_str):
        return some_str
    raise ValueError(f'{some_str} is not a valid email')


user_creation_parser = reqparse.RequestParser(bundle_errors=True)
user_creation_parser.add_argument('email', type=email_type, required=True)
user_creation_parser.add_argument('password', type=str, required=True)
user_creation_parser.add_argument('cellphone', type=str)
user_creation_parser.add_argument('first_name', type=str, required=True)
user_creation_parser.add_argument('last_name', type=str)
