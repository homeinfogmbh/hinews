"""Article handlers."""

from peewee import DoesNotExist

from his import ACCOUNT, DATA, authenticated, authorized
from his.messages import MissingData, InvalidData
from wsgilib import JSON

from hinews.messages.article import NoSuchArticle, ArticleCreated, \
    ArticleDeleted, ArticlePatched
from hinews.orm import InvalidElements, Article

__all__ = ['get_article', 'ROUTES']


def get_article(ident):
    """Returns the respective article."""

    try:
        return Article.get(Article.id == ident)
    except DoesNotExist:
        raise NoSuchArticle()


def set_tags(article, dictionary):
    """Sets the respective tags of the article iff specified."""

    try:
        article.tags = dictionary['tags']
    except KeyError:
        return []
    except InvalidElements as invalid_elements:
        return list(invalid_elements)

    return []


def set_customers(article, dictionary):
    """Sets the respective customers of the article iff specified."""

    try:
        article.customers = dictionary['customers']
    except KeyError:
        return []
    except InvalidElements as invalid_elements:
        return list(invalid_elements)

    return []


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

    dictionary = DATA.json

    try:
        article = Article.from_dict(
            ACCOUNT, dictionary, allow=('tags', 'customers'))
    except KeyError as key_error:
        raise MissingData(key=key_error.args[0])
    except ValueError as value_error:
        raise InvalidData(hint=value_error.args[0])

    article.save()
    invalid_tags = set_tags(article, dictionary)
    invalid_customers = set_customers(article, dictionary)

    return ArticleCreated(
        id=article.id, invalid_tags=invalid_tags,
        invalid_customers=invalid_customers)


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
    dictionary = DATA.json
    article.patch(dictionary, allow=('tags', 'customers'))
    article.save()
    article.editors.add(ACCOUNT)
    invalid_tags = set_tags(article, dictionary)
    invalid_customers = set_customers(article, dictionary)
    return ArticlePatched(
        invalid_tags=invalid_tags, invalid_customers=invalid_customers)


ROUTES = (
    ('GET', '/article', lst, 'list_articles'),
    ('GET', '/article/<int:ident>', get, 'get_article'),
    ('POST', '/article', post, 'post_article'),
    ('DELETE', '/article/<int:ident>', delete, 'delete_article'),
    ('PATCH', '/article/<int:ident>', patch, 'patch_article'))
