"""Article related messages."""

from hinews.messages.common import NewsMessage

__all__ = [
    'NoSuchArticle',
    'ArticleCreated',
    'ArticleDeleted',
    'ArticlePatched']


class NoSuchArticle(NewsMessage):
    """Indicates that the respective article does not exist."""

    STATUS = 404


class ArticleCreated(NewsMessage):
    """Indicates that the respective article was successfully created."""

    STATUS = 201


class ArticleDeleted(NewsMessage):
    """Indicates that the respective article was successfully deleted."""

    STATUS = 200


class ArticlePatched(NewsMessage):
    """Indicates that the respective article was successfully patched."""

    STATUS = 200
