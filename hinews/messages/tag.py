"""Tag related messages."""

from wsgilib import JSONMessage


__all__ = ['NO_SUCH_TAG', 'TAG_ADDED', 'TAG_DELETED', 'TAG_EXISTS']


NO_SUCH_TAG = JSONMessage('The requested tag does not exist.', status=404)
TAG_ADDED = JSONMessage('The tag has been added.', status=201)
TAG_DELETED = JSONMessage('The tag has been deleted.', status=200)
TAG_EXISTS = JSONMessage('The tag already exists.', status=409)
