"""WSGI application."""

from wsgilib import Application

from hinews.wsgi import article, customer, image, preview, public, tag


__all__ = ['APPLICATION']


APPLICATION = Application('hinews', debug=True, cors=True)
APPLICATION.add_routes(
    article.ROUTES + customer.ROUTES + image.ROUTES + preview.ROUTES
    + public.ROUTES + tag.ROUTES)
