"""Tag handlers."""

from flask import request

from his import authenticated, authorized
from wsgilib import JSON

from hinews.exceptions import InvalidTag
from hinews.messages.tag import NoSuchTag, TagAdded, TagDeleted
from hinews.orm import TagList, Tag
from hinews.wsgi.article import get_article


__all__ = ['ROUTES']


@authenticated
@authorized('hinews')
def list_():
    """Lists available tags."""

    return JSON([tag.tag for tag in TagList])


@authenticated
@authorized('hinews')
def get(ident):
    """Lists tags of the respective article."""

    return JSON([tag.to_dict() for tag in get_article(ident).tags])


@authenticated
@authorized('hinews')
def post(ident):
    """Adds a tag to the respective article."""

    article = get_article(ident)

    try:
        tag = Tag.add(article, request.data.decode())
    except InvalidTag:
        return NoSuchTag()

    tag.save()
    return TagAdded(id=tag.id)


@authenticated
@authorized('hinews')
def delete(article_id, tag_or_id):
    """Deletes the respective tag."""

    try:
        ident = int(tag_or_id)
    except ValueError:
        selection = (Tag.article == article_id) & (Tag.tag == tag_or_id)
    else:
        selection = (Tag.id == ident)

    try:
        tag = Tag.get(selection)
    except Tag.DoesNotExist:
        return TagDeleted()

    tag.delete_instance()
    return TagDeleted()


ROUTES = (
    ('GET', '/tags', list_, 'list_tags'),
    ('GET', '/article/<int:ident>/tags', get, 'get_tags'),
    ('POST', '/article/<int:ident>/tags', post, 'post_tag'),
    ('DELETE', '/article/<int:article_id>/tags/<tag>', delete, 'delete_tag'))
