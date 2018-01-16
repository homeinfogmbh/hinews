"""Article handlers."""

from his import SESSION, authenticated, authorized
from wsgilib import JSON, DATA

from hinews.orm import Article, ArticleImage

__all__ = ['get_article', 'ROUTES']


def get_article(ident):
    """Returns the respective article."""

    try:
        return Article.get(Article.id == ident)
    except DoesNotExist:
        raise NoSuchArticle()


@authenticated
@authorized('hinews')
def lst():
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

    article = Article.from_dict(SESSION.account, DATA.json)
    article.save()
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
    article.patch(DATA.json)
    article.save()
    article.editors.add(SESSION.account)
    return ArticlePatched()


ROUTES = (
    ('GET', '/article', lst, 'list_articles'),
    ('GET', '/article/<int:ident>', get, 'get_article'),
    ('POST', '/article', post, 'post_article'),
    ('DELETE', '/article/<int:ident>', delete, 'delete_article'),
    ('PATCH', '/article/<int:ident>', patch, 'patch_article'))
