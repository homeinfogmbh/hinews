"""Image related messages."""

from hinews.messages.facility import NEWS_MESSAGE


__all__ = [
    'NO_SUCH_IMAGE',
    'NO_IMAGE_PROVIDED',
    'NO_META_DATA_PROVIDED',
    'IMAGE_ADDED',
    'IMAGE_DELETED',
    'IMAGE_PATCHED']


NO_SUCH_IMAGE = NEWS_MESSAGE('The requested image does not exist.', status=404)
NO_IMAGE_PROVIDED = NEWS_MESSAGE('No image provided.', status=422)
NO_META_DATA_PROVIDED = NEWS_MESSAGE('No meta data provided.', status=422)
IMAGE_ADDED = NEWS_MESSAGE('The image has been added.', status=201)
IMAGE_DELETED = NEWS_MESSAGE('The image has been deleted.', status=200)
IMAGE_PATCHED = NEWS_MESSAGE(
    'The image meta data has been updated.', status=200)
