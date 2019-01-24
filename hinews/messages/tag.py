"""Tag related messages."""

from hinews.messages.facility import NEWS_MESSAGE


__all__ = ['NO_SUCH_TAG', 'TAG_ADDED', 'TAG_DELETED', 'TAG_EXISTS']


NO_SUCH_TAG = NEWS_MESSAGE('The requested tag does not exist.', status=404)
TAG_ADDED = NEWS_MESSAGE('The tag has been added.', status=201)
TAG_DELETED = NEWS_MESSAGE('The tag has been deleted.', status=200)
TAG_EXISTS = NEWS_MESSAGE('The tag already exists.', status=409)
