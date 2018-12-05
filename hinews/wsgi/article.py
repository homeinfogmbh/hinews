"""Article handlers."""

from flask import request

from his import ACCOUNT, authenticated, authorized
from wsgilib import JSON, Browser

from hinews.messages.article import ArticleCreated
from hinews.messages.article import ArticleDeleted
from hinews.messages.article import ArticlePatched
from hinews.messages.article import NoSuchArticle
from hinews.orm import article_active, Article, Editor


__all__ = ['get_article', 'ROUTES']


BROWSER = Browser(default_size=20)


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

    if 'all' in request.args:
        articles = Article
    elif 'inactive' in request.args:
        articles = Article.select().where(~ article_active())
    else:
        articles = Article.select().where(article_active())

    if BROWSER.info:
        return JSON(BROWSER.pages(articles).to_json())

    return JSON([article.to_json() for article in BROWSER.browse(articles)])


@authenticated
@authorized
def count():
    """Counts active and inactive articles."""

    active = Article.select().where(article_active())
    inactive = Article.select().where(~ article_active())
    return JSON({'active': len(active), 'inactive': len(inactive)})


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
    ('GET', '/article/count', count, 'count_articles'),
    ('GET', '/article/<int:ident>', get, 'get_article'),
    ('POST', '/article', post, 'post_article'),
    ('DELETE', '/article/<int:ident>', delete, 'delete_article'),
    ('PATCH', '/article/<int:ident>', patch, 'patch_article'))
