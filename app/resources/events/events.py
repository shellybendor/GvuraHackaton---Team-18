from flask import g
from app import db, auth
from sqlalchemy import and_
from http import HTTPStatus
from app.dal.models import Event, Changelog, Media
from flask_restful import Resource, marshal_with
from app.resources.events.events_utils import event_parser, event_search, event_update, nested_event_parser, \
    EVENTS_FILTERS
from app.resources.common import merge_new_tags
from app.dal.models.tag import TagRelevance
import app.resources.errors as errors


class Events(Resource):
    decorators = [auth.login_required]

    def post(self):
        args = event_parser.parse_args()

        event_with_same_title = Event.query.filter_by(title=args['title']).first()
        if event_with_same_title:
            raise errors.EventAlreadyExists

        tag_labels = set(args.pop('tags'))
        tags = merge_new_tags(tag_labels, TagRelevance.Events)
        medias = self._create_medias(set(args.pop('media')))
        title = args['title']
        first_update = Changelog(message=f'Created event "{title}"')
        event = Event(**args)
        event.tags.extend(tags)
        event.media.extend(medias)
        event.changelog.append(first_update)
        event.owners.append(g.user)

        try:
            db.session.add(event)
            db.session.commit()
        except:
            db.session.rollback()
            raise errors.InternalServerError

        return {
                   'id': event.id,
                   'title': event.title,
                   'qr_url': event.participation_secret_qr_url,
                   'status': first_update.message
               }, HTTPStatus.CREATED

    @marshal_with(Event.marshaller())
    def get(self, event_id=None):
        if event_id is not None:
            event = Event.query.get(event_id)
            if not event:
                raise errors.NoSuchEvent
            return event

        args = event_search.parse_args()
        limit = args.pop('limit')
        filters = [get_filter(args[key]) for key, get_filter in EVENTS_FILTERS.items() if key in args]
        return Event.query.filter(and_(*filters)).limit(limit).all(), HTTPStatus.OK

    @marshal_with(Event.marshaller())
    def patch(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            raise errors.NoSuchEvent

        authorized = self.authorized_for_event_changes(g.user, event)
        if not authorized:
            raise errors.NotAuthorized

        args = event_update.parse_args()
        update_args = nested_event_parser.parse_args(req=args)

        if update_args['title'] != event.title:
            event_with_same_title = Event.query.filter_by(title=update_args['title']).first()
            if event_with_same_title:
                raise errors.EventAlreadyExists

        for key, val in update_args.items():
            if val is not None:
                if key == 'tags':
                    setattr(event, key, merge_new_tags(val, TagRelevance.Events))
                    continue
                elif key == 'media':
                    setattr(event, key, [Media(url=url) for url in val])
                    continue
                elif key == 'participants':  # owner can't decide on participants
                    continue
                else:
                    setattr(event, key, val)

        event.changelog.append(Changelog(message=args['message'], updater_id=g.user.id))
        db.session.add(event)
        db.session.commit()
        return event, HTTPStatus.OK

    def delete(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            raise errors.NoSuchEvent

        authorized = self.authorized_for_event_changes(g.user, event)
        if not authorized:
            raise errors.NotAuthorized

        try:
            db.session.delete(event)
            db.session.commit()
            return {}, HTTPStatus.NO_CONTENT
        except:
            db.session.rollback()
            raise errors.InternalServerError

    @staticmethod
    def authorized_for_event_changes(user, event):
        role_authorized = any(role in ['admin', 'moderator'] for role in user.get_roles())
        ownership_authorized = user in event.owners
        return role_authorized or ownership_authorized

    @staticmethod
    def _create_medias(urls=[]):
        return [Media(type=None, url=url) for url in urls]
