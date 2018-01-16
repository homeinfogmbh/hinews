"""Article image handlers."""

from his import authenticated, authorized
from wsgilib import Binary, JSON

from hinews.wsgi.article import get_article

__all__ = ['ROUTES']


def get_image(ident):
    """Returns the respective image."""

    try:
        return ArticleImage.get(ArticleImage.id == ident)
    except DoesNotExist:
        raise NoSuchImage()


@authenticated
@authorized('hinews')
def lst(article_id):
    """Lists all available articles."""

    return JSON([image.to_dict() for image in get_article(article_id).images])


@authenticated
@authorized('hinews')
def get(ident):
    """Returns a specific article."""

    return Binary(get_image(ident).data)


@authenticated
@authorized('hinews')
def post(ident):
    """Adds a new article."""

    image = get_article(ident).images.add(DATA.bytes)
    return ImageAdded(image.id)


@authenticated
@authorized('hinews')
def delete(ident):
    """Adds a new article."""

    get_image(ident).delete_instance()
    return ImageDeleted()


@authenticated
@authorized('hinews')
def patch(ident):
    """Adds a new article."""

    image = get_image(ident)
    image.patch(DATA.json)
    image.save()
    return ImagePatched()


ROUTES = (
    ('GET', '/article/<int:ident>/images', lst, 'list_article_images'),
    ('GET', '/image/<int:ident>', get, 'get_image'),
    ('POST', '/article/<int:ident>/images', post, 'post_article_image'),
    ('DELETE', '/image/<int:ident>', delete, 'delete_image'),
    ('PATCH', '/image/<int:ident>', patch, 'patch_image'))
