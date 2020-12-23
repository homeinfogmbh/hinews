"""Image authentication for dscms3."""

from dscms3 import Users
from wsgilib import Binary

from hinews.messages.image import NO_SUCH_IMAGE
from hinews.orm import Image


__all__ = ['ROUTES']


@Users.authenticated
def get_image(ident):
    """Returns the respective image."""

    try:
        image = Image.get(Image.id == ident)
    except Image.DoesNotExist:
        raise NO_SUCH_IMAGE

    try:
        return Binary(image.watermarked)
    except OSError:     # Not an image.
        return Binary(image.bytes)


ROUTES = [('GET', '/dscms3/image/<int:ident>', get_image)]
