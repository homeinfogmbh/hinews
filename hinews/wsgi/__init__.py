"""WSGI application."""

from wsgilib import Application

from hinews.wsgi import article, customer, dscms3, image, preview, public, tag
from hinews.wsgi.local import APPLICATION as LOCAL_APPLICATION

__all__ = ['APPLICATION', 'LOCAL_APPLICATION']


APPLICATION = Application('hinews', debug=True, cors=True)
APPLICATION.add_routes(
    article.ROUTES + customer.ROUTES + dscms3.ROUTES + image.ROUTES
    + preview.ROUTES + public.ROUTES + tag.ROUTES)
