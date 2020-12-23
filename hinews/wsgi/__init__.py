"""WSGI application."""

from his import Application

from hinews.wsgi import article, customer, image, preview, public, tag
from hinews.wsgi.local import APPLICATION as LOCAL_APPLICATION


__all__ = ['APPLICATION', 'LOCAL_APPLICATION']


APPLICATION = Application('hinews', debug=True)
APPLICATION.add_routes(article.ROUTES)
APPLICATION.add_routes(customer.ROUTES)
APPLICATION.add_routes(image.ROUTES)
APPLICATION.add_routes(preview.ROUTES)
APPLICATION.add_routes(public.ROUTES)
APPLICATION.add_routes(tag.ROUTES)
