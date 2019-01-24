"""Article related messages."""

from hinews.messages.facility import NEWS_MESSAGE


__all__ = [
    'NO_SUCH_ARTICLE',
    'ARTICLE_CREATED',
    'ARTICLE_CREATED',
    'ARTICLE_PATCHED']


NO_SUCH_ARTICLE = NEWS_MESSAGE('This article does not exist.', status=404)
ARTICLE_CREATED = NEWS_MESSAGE('The article has been created.', status=201)
ARTICLE_DELETED = NEWS_MESSAGE('The article has been deleted.', status=200)
ARTICLE_PATCHED = NEWS_MESSAGE('The article has been updated.', status=200)
