"""Article image handlers."""

from json import loads

from flask import request

from his import ACCOUNT, authenticated, authorized
from his.messages.data import MISSING_DATA, INVALID_DATA
from wsgilib import Binary, JSON

from hinews.messages.image import IMAGE_ADDED
from hinews.messages.image import IMAGE_DELETED
from hinews.messages.image import IMAGE_PATCHED
from hinews.messages.image import NO_IMAGE_PROVIDED
from hinews.messages.image import NO_META_DATA_PROVIDED
from hinews.messages.image import NO_SUCH_IMAGE
from hinews.orm import Image
from hinews.wsgi.article import get_article


__all__ = ['ROUTES']


def get_image(ident):
    """Returns the respective image."""

    try:
        return Image.get(Image.id == ident)
    except Image.DoesNotExist:
        raise NO_SUCH_IMAGE


@authenticated
@authorized('hinews')
def list_():
    """Lists all available images."""

    return JSON([image.to_json() for image in Image])


@authenticated
@authorized('hinews')
def list_article_images(ident):
    """Lists all images of the respective articles."""

    return JSON([image.to_json() for image in get_article(ident).images])


@authenticated
@authorized('hinews')
def get(ident):
    """Returns a specific image."""

    return Binary(get_image(ident).bytes)


@authenticated
@authorized('hinews')
def post(ident):
    """Adds a new image to the respective article."""

    article = get_article(ident)

    try:
        image = request.files['image']
    except KeyError:
        raise NO_IMAGE_PROVIDED

    try:
        metadata = request.files['metadata']
    except KeyError:
        raise NO_META_DATA_PROVIDED

    with image.stream as stream:
        data = stream.read()

    with metadata.stream as stream:
        metadata = stream.read()

    metadata = loads(metadata.decode())

    try:
        image = Image.add(article, data, metadata, ACCOUNT.id)
    except KeyError as key_error:
        raise MISSING_DATA.update(key=key_error.args[0])
    except ValueError as value_error:
        raise INVALID_DATA.update(hint=value_error.args[0])

    image.file.save()
    image.save()
    return IMAGE_ADDED.update(id=image.id)


@authenticated
@authorized('hinews')
def delete(ident):
    """Deletes an image."""

    get_image(ident).delete_instance()
    return IMAGE_DELETED


@authenticated
@authorized('hinews')
def patch(ident):
    """Modifies image meta data."""

    image = get_image(ident)
    image.patch_json(request.json)
    image.save()
    return IMAGE_PATCHED


ROUTES = (
    ('GET', '/article/<int:ident>/images', list_article_images),
    ('POST', '/article/<int:ident>/images', post),
    ('GET', '/image', list_),
    ('GET', '/image/<int:ident>', get),
    ('DELETE', '/image/<int:ident>', delete),
    ('PATCH', '/image/<int:ident>', patch)
)
