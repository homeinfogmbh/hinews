"""Article customer controller."""

from flask import request

from his import authenticated, authorized
from wsgilib import JSON

from hinews.exceptions import InvalidCustomer
from hinews.messages.customer import NoSuchCustomer, CustomerAdded, \
    CustomerDeleted
from hinews.orm import CustomerList, ArticleCustomer
from hinews.wsgi.article import get_article


__all__ = ['ROUTES']


@authenticated
@authorized('hinews')
def list_():
    """Lists available customers."""

    return JSON([customer.to_dict() for customer in CustomerList])


@authenticated
@authorized('hinews')
def get(ident):
    """Lists customer of the respective article."""

    return JSON([
        customer.to_dict() for customer in get_article(ident).customers])


@authenticated
@authorized('hinews')
def post(ident):
    """Adds a customer to the respective article."""

    article = get_article(ident)

    try:
        customer = ArticleCustomer.add(article, request.data.decode())
    except InvalidCustomer:
        return NoSuchCustomer()

    customer.save()
    return CustomerAdded(id=customer.id)


@authenticated
@authorized('hinews')
def delete(article_id, customer_id):
    """Deletes the respective customer from the article."""

    ids = []

    for customer in ArticleCustomer.select().where(
            (ArticleCustomer.article == article_id)
            & (ArticleCustomer.customer == customer_id)):
        ids.append(customer.id)
        customer.delete_instance()

    return CustomerDeleted(ids=ids)


ROUTES = (
    ('GET', '/customers', list_, 'list_customers'),
    ('GET', '/article/<int:ident>/customers', get, 'get_customers'),
    ('POST', '/article/<int:ident>/customers', post, 'post_customer'),
    ('DELETE', '/article/<int:article_id>/customers/<customer_id>', delete,
     'delete_customer'))
