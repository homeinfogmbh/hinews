"""Image authentication for dscms3."""

from dscms3 import DSCMS3User
from wsgilib import Binary

from hinews.messages.image import NoSuchImage
from hinews.orm import Image


__all__ = ['ROUTES']


@DSCMS3User.authenticated
def get_image(ident):
    """Returns the respective image."""

    try:
        image = Image.get(Image.id == ident)
    except Image.DoesNotExist:
        raise NoSuchImage()

    try:
        return Binary(image.watermarked)
    except OSError:     # Not an image.
        return Binary(image.data)


ROUTES = (('GET', '/dscms3/image/<int:ident>', get_image, 'get_dscms3_image'),)
