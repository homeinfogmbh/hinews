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


def get_articles(customer):
    """Yields articles of the querying customer."""

    for article in Article:
        if article.active and customer in article.customers:
            yield article


def get_article(ident):
    """Yields articles of the querying customer."""

    try:
        article = Article.get(Article.id == ident)
    except DoesNotExist:
        raise NoSuchArticle()

    if get_customer() in article.customers:
        return article

    raise NoSuchArticle()


def get_image(ident):
    """Returns the respective image."""

    try:
        article_image = ArticleImage.get(ArticleImage.id == ident)
    except DoesNotExist:
        raise NoSuchImage()

    if get_customer() in article_image.article.customers:
        return article_image

    raise NoSuchArticle()


def lst():
    """Lists the respective news."""

    return JSON([article.to_dict() for article in get_articles(
        get_customer())])


def get(ident):
    """Returns the respective article."""

    return JSON(get_article(ident).to_dict())


def image(ident):
    """Returns the respective image."""

    return Binary(get_image(ident).data)


ROUTES = (
    ('GET', '/pub/article', lst, 'list_customer_articles'),
    ('GET', '/pub/article/<int:ident>', get, 'get_customer_article'),
    ('GET', '/pub/image/<int:ident>', image, 'get_customer_image'))
