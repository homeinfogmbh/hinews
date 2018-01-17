"""Article handlers."""

from peewee import DoesNotExist

from his import SESSION, DATA, authenticated, authorized
from his.messages import MissingData, InvalidData
from wsgilib import JSON

from hinews.messages.article import NoSuchArticle, ArticleCreated, \
    ArticleDeleted, ArticlePatched
from hinews.orm import Article

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

    try:
        article = Article.from_dict(SESSION.account, DATA.json)
    except KeyError as key_error:
        raise MissingData(key=key_error.args[0])
    except ValueError as value_error:
        raise InvalidData(hint=value_error.args[0])

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
