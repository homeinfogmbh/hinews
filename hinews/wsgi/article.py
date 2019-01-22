"""Article handlers."""

from flask import request

from his import ACCOUNT, authenticated, authorized
from wsgilib import JSON, Browser

from hinews.messages.article import ArticleCreated
from hinews.messages.article import ArticleDeleted
from hinews.messages.article import ArticlePatched
from hinews.messages.article import NoSuchArticle
from hinews.orm import article_active, Article, Editor, Tag


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

    condition = article_active()

    if 'inactive' in request.args:
        condition = ~condition

    articles = Article.select().where(condition).order_by(
        Article.created.desc())

    if BROWSER.info:
        return JSON(BROWSER.pages(articles).to_json())

    return JSON([article.to_json() for article in BROWSER.browse(articles)])


@authenticated
@authorized('hinews')
def search():
    """Searches for certain parameters."""
    customers = request.json.get('customers')
    tags = request.json.get('tags')
    active = request.json.get('active')
    match_customers = (Article.customer << customers) if customers else True
    match_tags = (Tag.tag << tags) if tags else True

    if active is None:
        match_active = True
    else:
        match_active = article_active() if active else (~ article_active())

    condition = match_active & match_customers & match_tags
    articles = Article.select().join(Tag).where(condition)

    if BROWSER.info:
        return JSON(BROWSER.pages(articles).to_json())

    return JSON([article.to_json() for article in BROWSER.browse(articles)])


@authenticated
@authorized('hinews')
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
    ('GET', '/articles', count, 'count_articles'),
    ('GET', '/article/<int:ident>', get, 'get_article'),
    ('POST', '/article', post, 'post_article'),
    ('POST', '/article/search', search, 'search_article'),
    ('DELETE', '/article/<int:ident>', delete, 'delete_article'),
    ('PATCH', '/article/<int:ident>', patch, 'patch_article'))
