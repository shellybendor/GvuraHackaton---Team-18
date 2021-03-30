from app.dal.models import Tag
from app.dal.models.tag import TagRelevance

from sqlalchemy import or_


def typed_list(item_type=int):
    def parse_list(list_str):
        return [item_type(i) for i in list_str.split(',')]

    return parse_list


def merge_new_tags(tag_labels, relevance):
    tag_filters = [Tag.label == label for label in tag_labels]
    existing_tags = Tag.query.filter(or_(*tag_filters)).all()
    existing_tags_labels = set([tag.label for tag in existing_tags])
    new_tags_labels = set(tag_labels) - existing_tags_labels
    new_tags = [Tag(label=label, relevance=relevance) for label in new_tags_labels]
    return list(existing_tags + new_tags)
