"""Customer related messages."""

from hinews.messages.facility import NEWS_MESSAGE


__all__ = ['CUSTOMER_ADDED', 'CUSTOMER_DELETED']


CUSTOMER_ADDED = NEWS_MESSAGE('The customer has been added.', status=201)
CUSTOMER_DELETED = NEWS_MESSAGE('The customer has been deleted.', status=200)
