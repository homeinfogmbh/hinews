"""ORM proxies."""

__all__ = ['Proxy', 'ArticleProxy']


class Proxy:
    """Proxy.to transparently handle data
    associated with the respective target.
    """

    def __init__(self, model, target):
        """Sets the model and target."""
        self.model = model
        self.target = target


class ArticleProxy(Proxy):
    """An article-related proxy."""

    def __iter__(self):
        """Yields sources of the respective article."""
        yield from self.model.select().where(self.model.article == self.target)

    def add(self, *args, **kwargs):
        """Adds the respective related model."""
        record = self.model.add(self.target, *args, **kwargs)
        record.save()
        return record

    def delete(self, ident):
        """Deletes the respective instance."""
        try:
            record = self.model.get(
                (self.model.article == self.target) & (self.model.id == ident))
        except self.model.DoesNotExist:
            return False

        return record.delete_instance()
