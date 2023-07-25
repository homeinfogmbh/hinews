"""HIS-internal preview."""

from typing import Iterable, Set

from peewee import Expression

from his import authenticated
from wsgilib import JSON, Binary

from hinews.messages.article import NO_SUCH_ARTICLE
from hinews.messages.image import NO_SUCH_IMAGE
from hinews.orm import article_active, Article, Tag, Image


__all__ = ["ROUTES"]


PREVIEW_TAGS = ("CMS",)


def _preview_article_ids() -> Set[int]:
    """Yields allowed preview articles."""

    return set(atag.article_id for atag in Tag.select().where(Tag.tag << PREVIEW_TAGS))


def _condition() -> Expression:
    """Returns the article selection condition."""

    return (Article.id << _preview_article_ids()) & article_active()


def _preview_articles() -> Iterable[Article]:
    """Yields allowed preview articles."""

    return Article.select().where(_condition()).order_by(Article.created).limit(4)


def _get_article(ident: int) -> Article:
    """Returns the respective preview article."""

    for article in _preview_articles():
        if article.id == ident:
            return article

    raise NO_SUCH_ARTICLE


def _get_image(ident: int) -> Image:
    """Returns the respective image."""

    try:
        image = Image.get(Image.id == ident)
    except Image.DoesNotExist:
        raise NO_SUCH_IMAGE from None

    if image.article in _preview_articles():
        return image

    raise NO_SUCH_IMAGE


@authenticated
def list_() -> JSON:
    """Lists the respective news."""

    return JSON([article.to_json(preview=True) for article in _preview_articles()])


@authenticated
def get_article(ident: int) -> JSON:
    """Returns the respective article."""

    return JSON(_get_article(ident).to_json(preview=True))


@authenticated
def get_image(ident: int) -> Binary:
    """Returns the respective image."""

    try:
        return Binary(_get_image(ident).watermarked)
    except OSError:  # Not an image.
        return Binary(_get_image(ident).bytes)


ROUTES = (
    ("GET", "/preview/article", list_),
    ("GET", "/preview/article/<int:ident>", get_article),
    ("GET", "/preview/image/<int:ident>", get_image),
)
