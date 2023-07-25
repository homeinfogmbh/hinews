"""Article related messages."""

from wsgilib import JSONMessage


__all__ = ["NO_SUCH_ARTICLE", "ARTICLE_CREATED", "ARTICLE_CREATED", "ARTICLE_PATCHED"]


NO_SUCH_ARTICLE = JSONMessage("This article does not exist.", status=404)
ARTICLE_CREATED = JSONMessage("The article has been created.", status=201)
ARTICLE_DELETED = JSONMessage("The article has been deleted.", status=200)
ARTICLE_PATCHED = JSONMessage("The article has been updated.", status=200)
