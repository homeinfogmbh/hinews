"""Article image handlers."""

from json import loads

from flask import request

from his import ACCOUNT, authenticated, authorized
from his.messages import MissingData, InvalidData
from wsgilib import Binary, JSON

from hinews.messages.image import NoSuchImage, NoImageProvided, \
    NoMetaDataProvided, ImageAdded, ImageDeleted, ImagePatched
from hinews.orm import ArticleImage
from hinews.wsgi.article import get_article

__all__ = ['ROUTES']


def get_image(ident):
    """Returns the respective image."""

    try:
        return ArticleImage.get(ArticleImage.id == ident)
    except ArticleImage.DoesNotExist:
        raise NoSuchImage()


@authenticated
@authorized('hinews')
def list_():
    """Lists all available images."""

    return JSON([image.to_dict() for image in ArticleImage])


@authenticated
@authorized('hinews')
def list_article_images(ident):
    """Lists all images of the respective articles."""

    return JSON([image.to_dict() for image in get_article(ident).images])


@authenticated
@authorized('hinews')
def get(ident):
    """Returns a specific image."""

    return Binary(get_image(ident).data)


@authenticated
@authorized('hinews')
def post(ident):
    """Adds a new image to the respective article."""

    try:
        image = request.files['image']
    except KeyError:
        raise NoImageProvided()

    try:
        metadata = request.files['metadata']
    except KeyError:
        raise NoMetaDataProvided()

    with image.stream as stream:
        data = stream.read()

    with metadata.stream as stream:
        metadata = stream.read()

    metadata = loads(metadata.decode())

    try:
        image = get_article(ident).images.add(data, metadata, ACCOUNT)
    except KeyError as key_error:
        raise MissingData(key=key_error.args[0])
    except ValueError as value_error:
        raise InvalidData(hint=value_error.args[0])

    return ImageAdded(id=image.id)


@authenticated
@authorized('hinews')
def delete(ident):
    """Deletes an image."""

    get_image(ident).delete_instance()
    return ImageDeleted()


@authenticated
@authorized('hinews')
def patch(ident):
    """Modifies image meta data."""

    image = get_image(ident)
    image.patch(request.json)
    image.save()
    return ImagePatched()


ROUTES = (
    ('GET', '/article/<int:ident>/images', list_article_images,
     'list_article_images'),
    ('POST', '/article/<int:ident>/images', post, 'post_article_image'),
    ('GET', '/image', list_, 'list_images'),
    ('GET', '/image/<int:ident>', get, 'get_image'),
    ('DELETE', '/image/<int:ident>', delete, 'delete_image'),
    ('PATCH', '/image/<int:ident>', patch, 'patch_image'))
