from app import db
from sqlalchemy import func
from http import HTTPStatus

from flask_restful import Resource
from app.dal.models import Tag
from app.resources.tags.tags_utils import tag_parser, tag_search
import app.resources.errors as errors


class Tags(Resource):
    def post(self):
        args = tag_parser.parse_args()
        tag = Tag.query.filter_by(label=args['label'], relevance=args['relevance']).first()
        if tag:
            raise errors.TagAlreadyExists
        else:
            tag = Tag(**args)
            db.session.add(tag)
            db.session.commit()
            return {'label': tag.label}, HTTPStatus.CREATED

    def get(self):
        # TODO: check for relevancy types
        args = tag_search.parse_args()
        limit = args.pop('limit')
        offset = args.pop('offset')
        query = Tag.query.filter(func.lower(Tag.relevance) == func.lower(args['relevance'])).offset(offset).limit(limit)
        tags = query.all()
        return [tag.label for tag in tags], HTTPStatus.OK
