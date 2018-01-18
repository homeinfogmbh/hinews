"""Article customer controller."""

from peewee import DoesNotExist

from his import DATA, authenticated, authorized
from homeinfo.crm import Customer
from wsgilib import JSON

from hinews.messages.customer import NoSuchCustomer, CustomerAdded, \
    CustomerDeleted
from hinews.wsgi.article import get_article

__all__ = ['ROUTES']


def get_customer(cid):
    """Returns the respective customer."""

    try:
        return Customer.get(Customer.id == cid)
    except DoesNotExist:
        raise NoSuchCustomer()


@authenticated
@authorized('hinews')
def lst():
    """Lists available customers."""

    return JSON([customer.to_dict(cascade=True) for customer in Customer])


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

    get_article(ident).customers.add(get_customer(DATA.text))
    return CustomerAdded()


@authenticated
@authorized('hinews')
def delete(article_id, customer_id):
    """Deletes the respective customer from the article."""

    get_article(article_id).customers.delete(get_customer(customer_id))
    return CustomerDeleted()


ROUTES = (
    ('GET', '/customers', lst, 'list_customers'),
    ('GET', '/article/<int:ident>/customers', get, 'get_customers'),
    ('POST', '/article/<int:ident>/customers', post, 'post_customer'),
    ('DELETE', '/article/<int:article_id>/customers/<customer_id>', delete,
     'delete_customer'))
