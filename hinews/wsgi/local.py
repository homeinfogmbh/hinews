"""Local interface without authentication
or authorization for previews.
"""
from typing import Iterable, Union

from flask import request

from wsgilib import Application, JSON, XML, Binary

from hinews import dom  # pylint: disable=E0611
from hinews.messages.article import NO_SUCH_ARTICLE
from hinews.messages.image import NO_SUCH_IMAGE
from hinews.orm import article_active, Article, Image


__all__ = ["APPLICATION"]


APPLICATION = Application("hinews", debug=True)


def _get_articles() -> Iterable[Article]:
    """Yields articles of the querying customer."""

    return Article.select().where(article_active())


def _get_article(ident: int) -> Article:
    """Returns the respective article of the querying customer."""

    try:
        return Article.get(article_active() & (Article.id == ident))
    except Article.DoesNotExist:
        raise NO_SUCH_ARTICLE from None


def _get_image(ident: int) -> Image:
    """Returns the respective image."""

    try:
        return Image.get(Image.id == ident)
    except Image.DoesNotExist:
        raise NO_SUCH_IMAGE from None


def list_() -> Union[JSON, XML]:
    """Lists the respective news."""

    try:
        request.args["xml"]
    except KeyError:
        return JSON([article.to_json() for article in _get_articles()])

    news = dom.news()
    news.article = [article.to_dom() for article in _get_articles()]
    return XML(news)


def get_article(ident: int) -> JSON:
    """Returns the respective article."""

    return JSON(_get_article(ident).to_json())


def get_image(ident: int) -> Binary:
    """Returns the respective image."""

    try:
        return Binary(_get_image(ident).watermarked)
    except OSError:  # Not an image.
        return Binary(_get_image(ident).bytes)


ROUTES = (
    ("GET", "/hinews/article", list_),
    ("GET", "/hinews/article/<int:ident>", get_article),
    ("GET", "/hinews/image/<int:ident>", get_image),
)
APPLICATION.add_routes(ROUTES)
