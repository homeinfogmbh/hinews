"""Image related messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_IMAGE',
    'NO_IMAGE_PROVIDED',
    'NO_META_DATA_PROVIDED',
    'IMAGE_ADDED',
    'IMAGE_DELETED',
    'IMAGE_PATCHED']


NO_SUCH_IMAGE = JSONMessage('The requested image does not exist.', status=404)
NO_IMAGE_PROVIDED = JSONMessage('No image provided.', status=422)
NO_META_DATA_PROVIDED = JSONMessage('No meta data provided.', status=422)
IMAGE_ADDED = JSONMessage('The image has been added.', status=201)
IMAGE_DELETED = JSONMessage('The image has been deleted.', status=200)
IMAGE_PATCHED = JSONMessage(
    'The image meta data has been updated.', status=200)
