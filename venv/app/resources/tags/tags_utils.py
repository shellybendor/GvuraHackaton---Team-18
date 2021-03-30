from flask_restful import reqparse
from app.dal.models.tag import TagRelevance
from app.resources.common import typed_list

tag_parser = reqparse.RequestParser(bundle_errors=True)
tag_parser.add_argument('label', type=str, required=True)
tag_parser.add_argument('relevance', type=lambda v: getattr(TagRelevance, v.capitalize()), required=True)

tag_search = reqparse.RequestParser()
tag_search.add_argument('relevance', location='args', store_missing=False, required=True)
tag_search.add_argument('limit', type=int, location='args', default=50)
tag_search.add_argument('offset', type=int, location='args', default=0)
