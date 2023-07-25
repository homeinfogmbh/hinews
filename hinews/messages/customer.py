"""Customer related messages."""

from wsgilib import JSONMessage


__all__ = ["CUSTOMER_ADDED", "CUSTOMER_DELETED"]


CUSTOMER_ADDED = JSONMessage("The customer has been added.", status=201)
CUSTOMER_DELETED = JSONMessage("The customer has been deleted.", status=200)
