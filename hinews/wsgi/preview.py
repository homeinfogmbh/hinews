"""HIS-internal preview."""

from his import authenticated
from wsgilib import JSON, Binary

from hinews.messages.article import NoSuchArticle
from hinews.messages.image import NoSuchImage
from hinews.orm import ArticleTag, ArticleImage

__all__ = ['ROUTES']


def _preview_articles():
    """Yields allowed preview articles."""

    for article_tag in ArticleTag.select().where(ArticleTag.tag == 'CMS'):
        yield article_tag.article


def _get_article(ident):
    """Returns the respective preview article."""

    for article in _preview_articles():
        if article.id == ident:
            return article

    raise NoSuchArticle()


def _get_image(ident):
    """Returns the respective image."""

    try:
        article_image = ArticleImage.get(ArticleImage.id == ident)
    except ArticleImage.DoesNotExist:
        raise NoSuchImage()

    if article_image.article in _preview_articles():
        return article_image

    raise NoSuchImage()


@authenticated
def list_():
    """Lists the respective news."""

    return JSON([article.to_dict() for article in _preview_articles()])


@authenticated
def get_article(ident):
    """Returns the respective article."""

    return JSON(_get_article(ident).to_dict())


@authenticated
def get_image(ident):
    """Returns the respective image."""

    try:
        return Binary(_get_image(ident).watermarked)
    except OSError:     # Not an image.
        return Binary(_get_image(ident).data)


ROUTES = (
    ('GET', '/preview/article', list_, 'list_preview_articles'),
    ('GET', '/preview/article/<int:ident>', get_article,
     'get_preview_article'),
    ('GET', '/preview/image/<int:ident>', get_image, 'get_preview_image'))
