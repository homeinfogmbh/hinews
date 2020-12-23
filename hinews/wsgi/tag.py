"""Tag handlers."""

from typing import Union

from flask import request

from his import authenticated, authorized, root
from wsgilib import JSON, JSONMessage

from hinews.exceptions import InvalidTag
from hinews.messages.tag import NO_SUCH_TAG, TAG_ADDED, TAG_DELETED, TAG_EXISTS
from hinews.orm import TagList, Tag
from hinews.wsgi.article import get_article


__all__ = ['ROUTES']


@authenticated
@authorized('hinews')
def list_() -> JSON:
    """Lists available tags."""

    return JSON([tag.tag for tag in TagList])


@authenticated
@authorized('hinews')
def get(ident: int) -> JSON:
    """Lists tags of the respective article."""

    return JSON([tag.to_json() for tag in get_article(ident).tags])


@authenticated
@authorized('hinews')
@root
def add() -> JSONMessage:
    """Adds a new tag to the list of registered tags."""

    tag = request.data.decode().strip()

    try:
        tag = TagList.get(TagList.tag == tag)
    except TagList.DoesNotExist:
        tag = TagList(tag=tag)
        tag.save()
        return TAG_ADDED.update(id=tag.id)

    return TAG_EXISTS.update(id=tag.id)


@authenticated
@authorized('hinews')
def post(ident: int) -> JSONMessage:
    """Adds a tag to the respective article."""

    article = get_article(ident)

    try:
        tag = Tag.add(article, request.data.decode())
    except InvalidTag:
        return NO_SUCH_TAG

    tag.save()
    return TAG_ADDED.update(id=tag.id)


@authenticated
@authorized('hinews')
def delete(article_id: int, tag_or_id: Union[str, int]) -> JSONMessage:
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
        return TAG_DELETED

    tag.delete_instance()
    return TAG_DELETED


ROUTES = (
    ('GET', '/tags', list_),
    ('POST', '/tags', add),
    ('GET', '/article/<int:ident>/tags', get),
    ('POST', '/article/<int:ident>/tags', post),
    ('DELETE', '/article/<int:article_id>/tags/<tag>', delete)
)
