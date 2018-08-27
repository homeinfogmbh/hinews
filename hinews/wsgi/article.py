"""Article handlers."""

from flask import request

from his import ACCOUNT, authenticated, authorized
from wsgilib import browse, JSON

from hinews.messages.article import NoSuchArticle, ArticleCreated, \
    ArticleDeleted, ArticlePatched
from hinews.orm import Article, Editor


__all__ = ['get_article', 'ROUTES']


def get_article(ident):
    """Returns the respective article."""

    try:
        return Article.get(Article.id == ident)
    except Article.DoesNotExist:
        raise NoSuchArticle()


@authenticated
@authorized('hinews')
def list_():
    """Lists all available articles."""

    return JSON([article.to_json() for article in browse(Article)])


@authenticated
@authorized('hinews')
def get(ident):
    """Returns a specific article."""

    return JSON(get_article(ident).to_json())


@authenticated
@authorized('hinews')
def post():
    """Adds a new article."""

    json = request.json
    tags = json.pop('tags', None)
    customers = json.pop('customers', None)
    article = Article.from_json(json, ACCOUNT.id, fk_fields=False)
    article.save()

    for tag in article.update_tags(tags):
        tag.save()

    for customer in article.update_customers(customers):
        customer.save()

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
    json = request.json
    tags = json.pop('tags', None)
    customers = json.pop('customers', None)
    article.patch_json(json, fk_fields=False)
    article.save()

    for tag in article.update_tags(tags):
        tag.save()

    for customer in article.update_customers(customers):
        customer.save()

    new_editor = Editor.add(article, ACCOUNT.id)
    new_editor.save()
    return ArticlePatched()


ROUTES = (
    ('GET', '/article', list_, 'list_articles'),
    ('GET', '/article/<int:ident>', get, 'get_article'),
    ('POST', '/article', post, 'post_article'),
    ('DELETE', '/article/<int:ident>', delete, 'delete_article'),
    ('PATCH', '/article/<int:ident>', patch, 'patch_article'))
