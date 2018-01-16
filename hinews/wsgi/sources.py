"""Article sources handlers."""

from wsgilib import DATA, JSON

from hinews.orm import ArticleSource
from hinews.wsgi.article import get_article

__all__ = ['ROUTES']


def get_article_source(ident):
    """Returns the respective article source."""

    try:
        return ArticleSource.get(ArticleSource.id == ident)
    except DoesNotExist:
        raise NoSuchArticleSource()


@authorized
@authenticated('hinews')
def get(ident):
    """Returns a specific article source."""

    return JSON(get_article_source(ident).to_dict())


@authorized
@authenticated('hinews')
def post(ident):
    """Adds an article source."""

    article_source = get_article(ident).sources.add(DATA.text)
    return ArticleSourceAdded(id=article_source.id)


@authorized
@authenticated('hinews')
def delete(ident):
    """Deletes the respective article source."""

    get_article_source(ident).delete_instance()
    return ArticleSourceDeleted()


ROUTES = (
    ('GET', '/article/<int:ident>/sources', lst, 'list_article_sources'),
    ('GET', '/source/<int:ident>', get, 'get_article_source'),
    ('POST', '/article/<int:ident>/sources', post, 'post_article_source'),
    ('DELETE', '/source/<int:ident>', delete, 'delete_article_source'))
