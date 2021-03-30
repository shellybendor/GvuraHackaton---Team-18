from datetime import datetime
from flask_restful import reqparse
from app.dal.models import Story, Tag
from app.resources.common import typed_list

# Parsers
upload_story_parser = reqparse.RequestParser(bundle_errors=True) \
    .add_argument('title', type=str, required=True) \
    .add_argument('description', type=str) \
    .add_argument('text', type=str, required=True) \
    .add_argument('country', type=str) \
    .add_argument('date', type=datetime.fromisoformat) \
    .add_argument('tags', type=list, location='json', default=[]) \
    .add_argument('media', type=list, location='json', default=[])

story_search = reqparse.RequestParser() \
    .add_argument('limit', type=int, location='args', default=50) \
    .add_argument('occurred_after', type=datetime.fromisoformat, location='args', store_missing=False) \
    .add_argument('occurred_before', type=datetime.fromisoformat, location='args', store_missing=False) \
    .add_argument('ids', type=typed_list(int), location='args', store_missing=False) \
    .add_argument('tags_any', type=typed_list(str), location='args', store_missing=False) \
    .add_argument('tags_all', type=typed_list(str), location='args', store_missing=False) \
    .add_argument('country', type=str, location='args', store_missing=False) \
    .add_argument('text', type=str, location='args', store_missing=False) \
    .add_argument('title', type=str, location='args', store_missing=False) \
    .add_argument('owner', type=int, location='args', store_missing=False)


# Filters
STORIES_FILTERS = {
    'occurred_after': lambda value: Story.date >= value,
    'occurred_before': lambda value: Story.date <= value,
    'ids': lambda value: Story.id.in_(value),
    'tags_any': lambda value: Story.tags.any(Tag.label.in_(value)),
    'country': lambda country: Story.country.is_(country),
    'text': lambda text: Story.text.contains(text),
    'title': lambda title: Story.title.contains(title),
    'owner': lambda owner_id: Story.owner_id.is_(owner_id),
    'tags_all': lambda value: Story.tags.all(Tag.label.in_(value))  # TODO: doesn't work
}

