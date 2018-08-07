"""Common functions."""

from json import loads

from flask import request

from timelib import strpdate
from wsgilib import Error

from hinews.orm import article_active, Article, ArticleTag


__all__ = ['select_options']


def select_options():
    """Returns a selection expression for the articles."""

    selection = True

    if 'active' in request.args:
        selection &= article_active()

    since = request.args.get('since')

    if since is not None:
        with Error('Invalid date: {}.'.format(since)).convert(ValueError):
            since = strpdate(since)

        selection &= Article.active_from >= since

    until = request.args.get('until')

    if until is not None:
        with Error('Invalid date: {}.'.format(until)).convert(ValueError):
            until = strpdate(until)

        selection &= Article.active_until < until

    tags = request.args.get('tags')

    if tags is not None:
        tags = loads(tags)

        if not isinstance(tags, list):
            raise Error('Not a list: {}.'.format(tags))

        tags = ArticleTag.select().where(ArticleTag.tag >> tags)
        articles = set(tag.article_id for tag in tags)
        selection &= Article.id << articles

    return selection