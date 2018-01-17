"""WSGI application."""

from wsgilib import Application

from hinews.wsgi import article, image

APPLICATION = Application('hinews', debug=True, cors=True)
APPLICATION.add_routes(article.ROUTES + image.ROUTES)
