from flask import g
from app import db, auth
from sqlalchemy import and_
from http import HTTPStatus
from app.dal.models import Event, EventParticipation
from flask_restful import Resource, marshal_with
from app.resources.events.events_utils import participation_approval
import app.resources.errors as errors


class EventsParticipation(Resource):
    decorators = [auth.login_required]

    def post(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            raise errors.NoSuchEvent

        if g.user in event.owners:
            raise errors.CantParticipateInOwnEvent

        participation = EventParticipation.query.filter_by(participant_id=g.user.id, event_id=event_id).first()
        if participation:
            return {'message': 'Already signed up :)'}, HTTPStatus.OK

        participation = EventParticipation(event_id=event_id,
                                           participated_event=event,
                                           participant_id=g.user.id,
                                           participant=g.user
                                           )

        event.participants.append(participation)
        try:
            db.session.add(participation)
            db.session.commit()
        except:
            db.session.rollback()
            raise errors.InternalServerError

        return {'message': f'Signed up for {event.title} successfully'}, HTTPStatus.OK

    def put(self, event_id, participant_id):
        event = Event.query.get(event_id)
        if not event:
            raise errors.NoSuchEvent

        if g.user not in event.owners:
            raise errors.NotAuthorized

        participation = EventParticipation.query.filter_by(event_id=event_id, participant_id=participant_id).first()
        if not participation:
            raise errors.NoSuchParticipant

        args = participation_approval.parse_args()

        participation.count = args['count']
        participation.validated = True

        try:
            db.session.add(participation)
            db.session.commit()
        except:
            raise errors.InternalServerError

        return {'message': 'participation registered successfully'}, HTTPStatus.OK

    def delete(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            raise errors.NoSuchEvent

        participation = EventParticipation.query.filter_by(participant_id=g.user.id, event_id=event_id).first()
        if not participation:
            return {'message': 'You are already not participating in that event', 'event_id': event_id}, HTTPStatus.OK

        try:
            db.session.delete(participation)
            db.session.commit()
        except:
            raise errors.InternalServerError

        return {'message': 'Revoked application from event successfully', 'event_id': event_id}, HTTPStatus.OK
