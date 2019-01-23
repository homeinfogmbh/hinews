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


def _filter_customers(articles, cids):
    """Filters articles by customers."""

    cids = frozenset(cids)

    if not cids:
        yield from articles
        return

    for article in articles:
        article_cids = frozenset(customer.id for customer in article.customers)

        if not article_cids:
            yield article
        else:
            if article_cids & cids:
                yield article


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
    select = Article.select()
    active = request.json.get('active')

    if active is None:
        condition = True
    else:
        condition = article_active() if active else (~ article_active())

    tags = request.json.get('tags')

    if tags:
        select = select.join(Tag, on=Tag.article == Article.id)
        condition &= (Tag.tag << tags)

    cids = request.json.get('customers')
    articles = _filter_customers(select.where(condition), cids)

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
