"""Article handlers."""

from typing import Iterable, Iterator

from flask import request

from his import ACCOUNT, authenticated, authorized
from wsgilib import Browser, JSON, JSONMessage

from hinews.messages.article import ARTICLE_CREATED
from hinews.messages.article import ARTICLE_DELETED
from hinews.messages.article import ARTICLE_PATCHED
from hinews.messages.article import NO_SUCH_ARTICLE
from hinews.orm import article_active, Article, Editor, Tag


__all__ = ["get_article", "ROUTES"]


BROWSER = Browser(default_size=20)


def _filter_customers(
    articles: Iterable[Article], cids: Iterable[int]
) -> Iterator[Article]:
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


def get_article(ident: int) -> Article:
    """Returns the respective article."""

    try:
        return Article.get(Article.id == ident)
    except Article.DoesNotExist:
        raise NO_SUCH_ARTICLE from None


@authenticated
@authorized("hinews")
def list_() -> JSON:
    """Lists all available articles."""

    condition = article_active()

    if "inactive" in request.args:
        condition = ~condition

    articles = Article.select().where(condition).order_by(Article.created.desc())

    if BROWSER.info:
        return JSON(BROWSER.pages(articles).to_json())

    return JSON([article.to_json() for article in BROWSER.browse(articles)])


@authenticated
@authorized("hinews")
def search() -> JSON:
    """Searches for certain parameters."""
    select = Article.select()
    active = request.json.get("active")

    if active is None:
        condition = True
    else:
        condition = article_active() if active else (~article_active())

    tags = request.json.get("tags")

    if tags:
        select = select.join(Tag, on=Tag.article == Article.id)
        condition &= Tag.tag << tags

    cids = request.json.get("customers")
    articles = _filter_customers(select.where(condition), cids)

    if BROWSER.info:
        return JSON(BROWSER.pages(articles).to_json())

    return JSON([article.to_json() for article in BROWSER.browse(articles)])


@authenticated
@authorized("hinews")
def count() -> JSON:
    """Counts active and inactive articles."""

    active = Article.select().where(article_active())
    inactive = Article.select().where(~article_active())
    return JSON({"active": len(active), "inactive": len(inactive)})


@authenticated
@authorized("hinews")
def get(ident: int) -> JSON:
    """Returns a specific article."""

    return JSON(get_article(ident).to_json())


@authenticated
@authorized("hinews")
def post() -> JSONMessage:
    """Adds a new article."""

    json = request.json
    tags = json.pop("tags", None)
    customers = json.pop("customers", None)
    article = Article.from_json(json, ACCOUNT.id, fk_fields=False)
    article.save()

    for tag in article.update_tags(tags):
        tag.save()

    for customer in article.update_customers(customers):
        customer.save()

    return ARTICLE_CREATED.update(id=article.id)


@authenticated
@authorized("hinews")
def delete(ident: int) -> JSONMessage:
    """Adds a new article."""

    get_article(ident).delete_instance()
    return ARTICLE_DELETED


@authenticated
@authorized("hinews")
def patch(ident: int) -> JSONMessage:
    """Adds a new article."""

    article = get_article(ident)
    json = request.json
    tags = json.pop("tags", None)
    customers = json.pop("customers", None)
    article.patch_json(json, fk_fields=False)
    article.save()

    for tag in article.update_tags(tags):
        tag.save()

    for customer in article.update_customers(customers):
        customer.save()

    new_editor = Editor.add(article, ACCOUNT.id)
    new_editor.save()
    return ARTICLE_PATCHED


ROUTES = (
    ("GET", "/article", list_),
    ("GET", "/articles", count),
    ("GET", "/article/<int:ident>", get),
    ("POST", "/article", post),
    ("POST", "/article/search", search),
    ("DELETE", "/article/<int:ident>", delete),
    ("PATCH", "/article/<int:ident>", patch),
)
