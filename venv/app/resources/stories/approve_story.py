from flask import request
from http import HTTPStatus
from flask_restful import Resource

from app import db, auth
from app.dal.models import Story
from app.resources.errors import InternalServerError, NoSuchStory


class ApproveStory(Resource):
    decorators = [auth.login_required(role=['admin', 'moderator'])]

    def get(self, story_id):
        story = Story.query.get(story_id)

        if not story:
            raise NoSuchStory

        try:
            story.approved = True
            db.session.add(story)
            db.session.commit()
            return {"message": "success"}, HTTPStatus.OK
        except Exception:
            db.session.rollback()
            return InternalServerError
