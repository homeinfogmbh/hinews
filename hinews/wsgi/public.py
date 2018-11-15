"""Public customer interface without
HIS authentication or authorization.
"""
from flask import request

from wsgilib import ACCEPT, JSON, XML, Binary, Browser

from hinews import dom
from hinews.messages.article import NoSuchArticle
from hinews.messages.image import NoSuchImage
from hinews.messages.public import MissingAccessToken, InvalidAccessToken
from hinews.wsgi.functions import select_options
from hinews.orm import Article, Image, AccessToken


__all__ = ['ROUTES']


BROWSER = Browser()


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

    customer = _get_customer()

    for article in Article.select().where(select_options()):
        customers = article.customers

        if not customers or customer in customers:
            yield article


def _get_article(ident):
    """Returns the respective article of the querying customer."""

    customer = _get_customer()

    try:
        article = Article.get(Article.id == ident)
    except Article.DoesNotExist:
        raise NoSuchArticle()

    customers = article.customers

    if not customers or customer in customers:
        return article

    raise NoSuchArticle()


def _get_image(ident):
    """Returns the respective image."""

    customer = _get_customer()

    try:
        image = Image.get(Image.id == ident)
    except Image.DoesNotExist:
        raise NoSuchImage()

    customers = image.article.customers

    if not customers or customer in customers:
        return image

    raise NoSuchImage()


def list_():
    """Lists the respective news."""

    articles = _get_articles(_get_customer())

    if 'page' in request.args:
        articles = BROWSER.browse(articles)

    if 'application/json' in ACCEPT and 'xml' not in request.args:
        return JSON([article.to_json(preview=True) for article in articles])

    news = dom.news()
    news.article = [article.to_dom() for article in articles]
    return XML(news)


def get_article(ident):
    """Returns the respective article."""

    return JSON(_get_article(ident).to_json(preview=True))


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
