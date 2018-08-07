"""Customer related messages."""

from hinews.messages.common import NewsMessage


__all__ = ['NoSuchCustomer', 'CustomerAdded', 'CustomerDeleted']


class NoSuchCustomer(NewsMessage):
    """Indicates that the respective customer does not exist."""

    STATUS = 404


class CustomerAdded(NewsMessage):
    """Indicates that the respective customer was successfully added."""

    STATUS = 201


class CustomerDeleted(NewsMessage):
    """Indicates that the respective customer was deleted successfully."""

    STATUS = 200
