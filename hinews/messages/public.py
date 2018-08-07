"""Public API related messages."""

from hinews.messages.common import NewsMessage


__all__ = ['MissingAccessToken', 'InvalidAccessToken']


class MissingAccessToken(NewsMessage):
    """Indicates that no access token was provided."""

    STATUS = 422


class InvalidAccessToken(NewsMessage):
    """Indicates that the the access token is invalid."""

    STATUS = 422
