"""Public customer interface without
HIS authentication or authorization.
"""
from flask import request
from peewee import DoesNotExist

from wsgilib import JSON, Binary

from hinews.messages.article import NoSuchArticle
from hinews.messages.image import NoSuchImage
from hinews.messages.public import MissingAccessToken, InvalidAccessToken
from hinews.orm import Article, ArticleImage, AccessToken

__all__ = ['ROUTES']


def get_customer():
    """Returns the customer for the respective access token."""

    try:
        access_token = request.args['access_token']
    except KeyError:
        raise MissingAccessToken()

    try:
        access_token = AccessToken.get(AccessToken.token == access_token)
    except DoesNotExist:
        raise InvalidAccessToken()

    return access_token.customer


def get_articles():
    """Yields articles of the querying customer."""

    return Article.select().where(Article.customer == get_customer())


def get_article(ident):
    """Yields articles of the querying customer."""

    try:
        return Article.get(
            (Article.customer == get_customer()) & (Article.id == ident))
    except DoesNotExist:
        raise NoSuchArticle()


def get_image(ident):
    """Returns the respective image."""

    try:
        return ArticleImage.get(
            (ArticleImage.article.customer == get_customer())
            & (ArticleImage.id == ident))
    except DoesNotExist:
        raise NoSuchImage()


def lst():
    """Lists the respective news."""

    return JSON([article.id for article in get_articles()])


def get(ident):
    """Returns the respective article."""

    return JSON(get_article(ident).to_dict())


def image(ident):
    """Returns the respective image."""

    return Binary(get_image(ident).data)


ROUTES = (
    ('GET', '/pub/article', lst, 'list_articles'),
    ('GET', '/pub/article/<int:ident>', get, 'get_article'),
    ('GET', '/pub/image/<int:ident>', image, 'get_image'))
