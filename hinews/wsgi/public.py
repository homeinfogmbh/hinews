"""Public customer interface without
HIS authentication or authorization.
"""
from flask import request

from wsgilib import JSON, XML, Binary

from hinews import dom
from hinews.messages.article import NoSuchArticle
from hinews.messages.image import NoSuchImage
from hinews.messages.public import MissingAccessToken, InvalidAccessToken
from hinews.wsgi.functions import select_options
from hinews.orm import article_active, Article, Image, AccessToken, \
    ArticleCustomer


__all__ = ['ROUTES']


def _get_customer():
    """Returns the customer for the respective access token."""

    try:
        access_token = request.args['access_token']
    except KeyError:
        raise MissingAccessToken()

    try:
        access_token = AccessToken.get(AccessToken.token == access_token)
    except AccessToken.DoesNotExist:
        raise InvalidAccessToken()

    return access_token.customer


def _get_articles(customer):
    """Yields articles of the querying customer."""

    return Article.select().join(ArticleCustomer).where(
        (ArticleCustomer.customer == customer) & select_options())


def _get_article(ident):
    """Returns the respective article of the querying customer."""

    try:
        return Article.select().join(ArticleCustomer).where(
            (Article.id == ident)
            & (ArticleCustomer.customer == _get_customer())
            & article_active()).get()
    except Article.DoesNotExist:
        raise NoSuchArticle()


def _get_image(ident):
    """Returns the respective image."""

    try:
        return Image.select().join(Article).join(ArticleCustomer).where(
            (Image.id == ident)
            & (ArticleCustomer.customer == _get_customer())).get()
    except Image.DoesNotExist:
        raise NoSuchImage()


def list_():
    """Lists the respective news."""

    if 'xml' in request.args:
        news = dom.news()
        news.article = [article.to_dom() for article in _get_articles(
            _get_customer())]
        return XML(news)

    return JSON([
        article.to_dict(preview=True) for article in _get_articles(
            _get_customer())])


def get_article(ident):
    """Returns the respective article."""

    return JSON(_get_article(ident).to_dict(preview=True))


def get_image(ident):
    """Returns the respective image."""

    try:
        return Binary(_get_image(ident).watermarked)
    except OSError:     # Not an image.
        return Binary(_get_image(ident).data)


ROUTES = (
    ('GET', '/pub/article', list_, 'list_customer_articles'),
    ('GET', '/pub/article/<int:ident>', get_article, 'get_customer_article'),
    ('GET', '/pub/image/<int:ident>', get_image, 'get_customer_image'))
