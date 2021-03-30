from http import HTTPStatus

from flask import g
from flask_restful import Resource, marshal_with

from app import db, auth
from app.dal.models import Story, Media
from app.dal.models.tag import TagRelevance
from app.resources.stories.stories_utils import upload_story_parser, story_search, STORIES_FILTERS
from app.resources.common import merge_new_tags
import app.resources.errors as errors

from sqlalchemy import and_


class Stories(Resource):
    decorators = [auth.login_required]

    def post(self):
        args = upload_story_parser.parse_args()

        story_with_same_title = Story.query.filter_by(title=args['title']).first()
        if story_with_same_title:
            raise errors.StoryAlreadyExists

        medias = self._create_medias(set(args.pop('media')))
        tag_labels = set(args.pop('tags'))
        tags = merge_new_tags(tag_labels, TagRelevance.Stories)

        story = Story(**args)
        story.tags.extend(tags)
        story.media.extend(medias)
        story.owner_id = g.user.id

        try:
            db.session.add(story)
            db.session.commit()
        except:
            db.session.rollback()
            raise errors.InternalServerError

        return {"id": story.id,
                "title": story.title
                }, HTTPStatus.CREATED

    @marshal_with(Story.marshaller())
    def get(self, story_id=None):
        if story_id:
            story = Story.query.get(story_id)
            if not story:
                raise errors.NoSuchStory
            return story, HTTPStatus.OK

        args = story_search.parse_args()
        limit = args.pop('limit')
        filters = [get_filter(args[key]) for key, get_filter in STORIES_FILTERS.items() if key in args]
        return Story.query.filter(and_(*filters)).limit(limit).all(), HTTPStatus.OK

    @marshal_with(Story.marshaller())
    def patch(self, story_id):
        story = Story.query.get(story_id)
        if not story:
            raise errors.NoSuchStory

        authorized = self.authorized_for_story_changes(g.user, story_id)
        if not authorized:
            raise errors.NotAuthorized

        update_args = upload_story_parser.parse_args()

        if update_args['title'] != story.title:
            story_with_same_title = Story.query.filter_by(title=update_args['title']).first()
            if story_with_same_title:
                raise errors.StoryAlreadyExists

        for key, val in update_args.items():
            if key == 'tags':
                setattr(story, key, merge_new_tags(val, TagRelevance.Stories))
                continue
            elif key == 'media':
                setattr(story, key, [Media(url=url) for url in val])
                continue
            else:
                setattr(story, key, val)

        db.session.add(story)
        db.session.commit()
        return story, HTTPStatus.OK

    def delete(self, story_id):
        story = Story.query.get(story_id)
        if not story:
            raise errors.NoSuchStory

        authorized = self.authorized_for_story_changes(g.user, story_id)
        if not authorized:
            raise errors.NotAuthorized

        try:
            db.session.delete(story)
            db.session.commit()
            return {}, HTTPStatus.NO_CONTENT
        except:
            db.session.rollback()
            raise errors.InternalServerError

    @staticmethod
    def _create_medias(urls=[]):
        return [Media(type=None, url=url) for url in urls]

    @staticmethod
    def authorized_for_story_changes(user, story_id):
        role_authorized = any(role in ['admin', 'moderator'] for role in user.get_roles())
        ownership_authorized = Story.query.get(story_id).owner_id == user.id
        return role_authorized or ownership_authorized
