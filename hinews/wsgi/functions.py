"""Common functions."""

from json import loads

from flask import request

from timelib import strpdate
from wsgilib import Error

from hinews.orm import article_active, Article, Tag


__all__ = ['select_options']


def select_options():
    """Returns a selection expression for the articles."""

    if 'all' in request.args:
        selection = True
    else:
        selection = article_active()

    since = request.args.get('since')

    if since is not None:
        try:
            since = strpdate(since)
        except ValueError:
            raise Error(f'Invalid date: {since}')

        selection &= Article.active_from >= since

    until = request.args.get('until')

    if until is not None:
        try:
            until = strpdate(until)
        except ValueError:
            raise Error(f'Invalid date: {until}')

        selection &= Article.active_until < until

    tags = request.args.get('tags')

    if tags is not None:
        tags = loads(tags)

        if not isinstance(tags, list):
            raise Error(f'Not a list: {tags}')

        tags = Tag.select().where(Tag.tag >> tags)
        articles = set(tag.article_id for tag in tags)
        selection &= Article.id << articles

    return selection
