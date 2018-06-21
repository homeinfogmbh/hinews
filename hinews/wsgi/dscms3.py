"""Image authentication for dscms3."""

from homeinfo.dscms3 import DSCMS3User
from wsgilib import Binary

from hinews.messages.image import NoSuchImage
from hinews.orm import ArticleImage

__all__ = ['ROUTES']


@DSCMS3User.authenticated
def get_image(ident):
    """Returns the respective image."""

    try:
        image = ArticleImage.get(ArticleImage.id == ident)
    except ArticleImage.DoesNotExist:
        raise NoSuchImage()

    try:
        return Binary(image.watermarked)
    except OSError:     # Not an image.
        return Binary(image.data)


ROUTES = (('GET', '/dscms3/<int:ident>', get_image, 'get_dscms3_image'),)
