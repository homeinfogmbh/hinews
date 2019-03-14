"""Public API related messages."""

from wsgilib import JSONMessage


__all__ = ['MISSING_ACCESS_TOKEN', 'INVALID_ACCESS_TOKEN']


MISSING_ACCESS_TOKEN = JSONMessage('No access token provided.', status=401)
INVALID_ACCESS_TOKEN = JSONMessage('Invalid access token.', status=403)
