from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.resources.errors import auth_error_dict
from app.resources.errors import errors
from config import Config

db = SQLAlchemy()
api = Api(errors=errors)
auth = HTTPBasicAuth()  # No need to initialize with app


@auth.error_handler
def auth_error(status):
    return jsonify(auth_error_dict), status


def create_app(config_class=Config):
    from app.resources.tags import Tags
    from app.resources.events import Events
    from app.resources.events.events_participation import EventsParticipation
    from app.resources.authentication import User, APIToken
    from app.resources.stories.stories import Stories
    from app.resources.stories.approve_story import ApproveStory

    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    if app.debug or app.testing:
        db.create_all(app=app)
    api.add_resource(User, '/user', '/user/<int:user_id>')
    api.add_resource(APIToken, '/token')

    api.add_resource(Events, '/events', '/events/<int:event_id>')
    api.add_resource(EventsParticipation, '/participation/<int:event_id>',
                     '/participation/<int:event_id>/<int:participant_id>')
    api.add_resource(Stories, '/stories', '/stories/<int:story_id>')
    api.add_resource(ApproveStory, '/approve/story/<int:story_id>')

    api.add_resource(Tags, '/tags')
    # noinspection PyTypeChecker
    api.init_app(app)
    return app
