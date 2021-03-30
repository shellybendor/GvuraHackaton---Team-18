from datetime import datetime
from flask_restful import reqparse
from app.dal.models import Event, Tag
from app.resources.common import typed_list

# Parsers
event_parser = reqparse.RequestParser() \
    .add_argument('geolocation') \
    .add_argument('title') \
    .add_argument('description') \
    .add_argument('start_time', type=datetime.fromisoformat) \
    .add_argument('end_time', type=datetime.fromisoformat) \
    .add_argument('reward', type=int) \
    .add_argument('tags', type=list, location='json', default=[]) \
    .add_argument('media', type=list, location='json', default=[])

nested_event_parser = reqparse.RequestParser() \
    .add_argument('geolocation', location=('event_data',)) \
    .add_argument('title', location=('event_data',)) \
    .add_argument('description', location=('event_data',)) \
    .add_argument('start_time', type=datetime.fromisoformat, location=('event_data',)) \
    .add_argument('end_time', type=datetime.fromisoformat, location=('event_data',)) \
    .add_argument('reward', type=int, location=('event_data',)) \
    .add_argument('tags', type=typed_list(str), location=('event_data',), default=[]) \
    .add_argument('media', type=typed_list(str), location=('event_data',), default=[])

event_search = reqparse.RequestParser() \
    .add_argument('limit', type=int, location='args', default=50) \
    .add_argument('starts_after', type=datetime.fromisoformat, location='args', store_missing=False) \
    .add_argument('starts_before', type=datetime.fromisoformat, location='args', store_missing=False) \
    .add_argument('ids', type=typed_list(int), location='args', store_missing=False) \
    .add_argument('tags_any', type=typed_list(str), location='args', store_missing=False) \
    .add_argument('tags_all', type=typed_list(str), location='args', store_missing=False)

event_update = reqparse.RequestParser() \
    .add_argument('event_data', type=dict, location='json', required=True) \
    .add_argument('message', required=True) \
    .add_argument('cancel', type=str)

participation_approval = reqparse.RequestParser() \
    .add_argument('count', type=int, default=1)

# Filters
EVENTS_FILTERS = {
    'starts_after': lambda value: Event.start_time >= value,
    'starts_before': lambda value: Event.start_time <= value,
    'ids': lambda value: Event.id.in_(value),
    'tags_any': lambda value: Event.tags.any(Tag.label.in_(value)),
    'tags_all': lambda value: Event.tags.all(Tag.label.in_(value))  # TODO: doesn't work
}
