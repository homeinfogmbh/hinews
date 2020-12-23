"""Public customer interface without
HIS authentication or authorization.
"""
from typing import Iterator, Union

from flask import request

from mdb import Customer
from wsgilib import ACCEPT, JSON, XML, Binary, Browser

from hinews import dom  # pylint: disable=E0611
from hinews.messages.article import NO_SUCH_ARTICLE
from hinews.messages.image import NO_SUCH_IMAGE
from hinews.messages.public import MISSING_ACCESS_TOKEN, INVALID_ACCESS_TOKEN
from hinews.wsgi.functions import select_options
from hinews.orm import Article, Image, AccessToken


__all__ = ['ROUTES']


BROWSER = Browser()


def _get_customer() -> Customer:
    """Returns the customer for the respective access token."""

    try:
        access_token = request.args['access_token']
    except KeyError:
        raise MISSING_ACCESS_TOKEN from None

    try:
        access_token = AccessToken.get(AccessToken.token == access_token)
    except AccessToken.DoesNotExist:
        raise INVALID_ACCESS_TOKEN from None

    return access_token.customer


def _get_articles(customer: Customer) -> Iterator[Article]:
    """Yields articles of the querying customer."""

    customer = _get_customer()

    for article in Article.select().where(select_options()):
        customers = article.customers

        if not customers or customer in customers:
            yield article


def _get_article(ident: int) -> Article:
    """Returns the respective article of the querying customer."""

    customer = _get_customer()

    try:
        article = Article.get(Article.id == ident)
    except Article.DoesNotExist:
        raise NO_SUCH_ARTICLE from None

    customers = article.customers

    if not customers or customer in customers:
        return article

    raise NO_SUCH_ARTICLE


def _get_image(ident: int) -> Image:
    """Returns the respective image."""

    customer = _get_customer()

    try:
        image = Image.get(Image.id == ident)
    except Image.DoesNotExist:
        raise NO_SUCH_IMAGE from None

    customers = image.article.customers

    if not customers or customer in customers:
        return image

    raise NO_SUCH_IMAGE


def list_() -> Union[JSON, XML]:
    """Lists the respective news."""

    articles = _get_articles(_get_customer())

    if 'page' in request.args:
        articles = BROWSER.browse(articles)

    if 'application/json' in ACCEPT and 'xml' not in request.args:
        return JSON([article.to_json(preview=True) for article in articles])

    news = dom.news()
    news.article = [article.to_dom() for article in articles]
    return XML(news)


def get_article(ident: int) -> JSON:
    """Returns the respective article."""

    return JSON(_get_article(ident).to_json(preview=True))


def get_image(ident: int) -> Binary:
    """Returns the respective image."""

    try:
        return Binary(_get_image(ident).watermarked)
    except OSError:     # Not an image.
        return Binary(_get_image(ident).bytes)


ROUTES = (
    ('GET', '/pub/article', list_),
    ('GET', '/pub/article/<int:ident>', get_article),
    ('GET', '/pub/image/<int:ident>', get_image)
)
