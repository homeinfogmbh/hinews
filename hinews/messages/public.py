"""Public API related messages."""

from hinews.messages.facility import NEWS_MESSAGE


__all__ = ['MISSING_ACCESS_TOKEN', 'INVALID_ACCESS_TOKEN']


MISSING_ACCESS_TOKEN = NEWS_MESSAGE('No access token provided.', status=401)
INVALID_ACCESS_TOKEN = NEWS_MESSAGE('Invalid access token.', status=403)
