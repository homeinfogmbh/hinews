"""Common functions."""

from datetime import date
from json import loads

from flask import request
from peewee import Expression

from wsgilib import Error

from hinews.orm import article_active, Article, Tag


__all__ = ["select_options"]


def select_options() -> Expression:
    """Returns a condition expression for the articles."""

    if "all" in request.args:
        condition = True
    else:
        condition = article_active()

    since = request.args.get("since")

    if since is not None:
        try:
            since = date.fromisoformat(since)
        except ValueError:
            raise Error(f"Invalid date: {since}") from None

        condition &= Article.active_from >= since

    until = request.args.get("until")

    if until is not None:
        try:
            until = date.fromisoformat(until)
        except ValueError:
            raise Error(f"Invalid date: {until}") from None

        condition &= Article.active_until < until

    tags = request.args.get("tags")

    if tags is not None:
        tags = loads(tags)

        if not isinstance(tags, list):
            raise Error(f"Not a list: {tags}")

        tags = Tag.select().where(Tag.tag >> tags)
        articles = set(tag.article_id for tag in tags)
        condition &= Article.id << articles

    return condition
