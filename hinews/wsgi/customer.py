"""Article customer controller."""

from flask import request

from his import authenticated, authorized
from wsgilib import JSON, JSONMessage

from hinews.messages.customer import CUSTOMER_ADDED, CUSTOMER_DELETED
from hinews.orm import AccessToken, Whitelist
from hinews.wsgi.article import get_article


__all__ = ["ROUTES"]


@authenticated
@authorized("hinews")
def list_() -> JSON:
    """Lists available customers."""

    customers = set(access_token.customer for access_token in AccessToken)
    return JSON([customer.to_json() for customer in customers])


@authenticated
@authorized("hinews")
def get(ident: int) -> JSON:
    """Lists customer of the respective article."""

    return JSON([customer.to_json() for customer in get_article(ident).customers])


@authenticated
@authorized("hinews")
def post(ident: int) -> JSONMessage:
    """Adds a customer to the respective article."""

    article = get_article(ident)
    customer = Whitelist.add(article, request.data.decode())
    customer.save()
    return CUSTOMER_ADDED.update(id=customer.id)


@authenticated
@authorized("hinews")
def delete(article_id: int, customer_id: int) -> JSONMessage:
    """Deletes the respective customer from the article."""

    ids = []

    for customer in Whitelist.select().where(
        (Whitelist.article == article_id) & (Whitelist.customer == customer_id)
    ):
        ids.append(customer.id)
        customer.delete_instance()

    return CUSTOMER_DELETED.update(ids=ids)


ROUTES = (
    ("GET", "/customers", list_),
    ("GET", "/article/<int:ident>/customers", get),
    ("POST", "/article/<int:ident>/customers", post),
    ("DELETE", "/article/<int:article_id>/customers/<customer_id>", delete),
)
