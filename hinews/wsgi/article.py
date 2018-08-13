"""Article handlers."""

from flask import request

from his import ACCOUNT, authenticated, authorized
from his.messages import MissingData, InvalidData
from peeweeplus import FieldValueError, FieldNotNullable
from wsgilib import JSON

from hinews.messages.article import NoSuchArticle, ArticleCreated, \
    ArticleDeleted, ArticlePatched
from hinews.orm import Article, Editor


__all__ = ['get_article', 'ROUTES']


def get_article(ident):
    """Returns the respective article."""

    try:
        return Article.get(Article.id == ident)
    except Article.DoesNotExist:
        raise NoSuchArticle()


@authenticated
@authorized('hinews')
def list_():
    """Lists all available articles."""

    return JSON([article.to_dict() for article in Article])


@authenticated
@authorized('hinews')
def get(ident):
    """Returns a specific article."""

    return JSON(get_article(ident).to_dict())


@authenticated
@authorized('hinews')
def post():
    """Adds a new article."""

    try:
        article, *related_records = Article.from_dict(
            ACCOUNT.id, request.json, fk_fields=False)
        article.save()

        for record in related_records:
            record.save()
    except FieldNotNullable as field_not_nullable:
        raise MissingData(**field_not_nullable.to_dict())
    except FieldValueError as field_value_error:
        raise InvalidData(**field_value_error.to_dict())

    return ArticleCreated(id=article.id)


@authenticated
@authorized('hinews')
def delete(ident):
    """Adds a new article."""

    get_article(ident).delete_instance()
    return ArticleDeleted()


@authenticated
@authorized('hinews')
def patch(ident):
    """Adds a new article."""

    article = get_article(ident)
    article, *related_records = article.patch(request.json, fk_fields=False)
    article.save()

    for record in related_records:
        record.save()

    new_editor = Editor.add(article, ACCOUNT.id)
    new_editor.save()
    return ArticlePatched()


ROUTES = (
    ('GET', '/article', list_, 'list_articles'),
    ('GET', '/article/<int:ident>', get, 'get_article'),
    ('POST', '/article', post, 'post_article'),
    ('DELETE', '/article/<int:ident>', delete, 'delete_article'),
    ('PATCH', '/article/<int:ident>', patch, 'patch_article'))
