"""Exceptions."""

__all__ = ['InvalidCustomer', 'InvalidElements', 'InvalidTag']


class InvalidCustomer(Exception):
    """Indicates that a respective tag is not registered."""

    pass


class InvalidElements(Exception):
    """Indicates that the respective elements are invalid."""

    def __init__(self, elements):
        """Sets the invalid elements."""
        super().__init__(elements)
        self.elements = elements

    def __iter__(self):
        """Yields the invalid elements."""
        yield from self.elements


class InvalidTag(Exception):
    """Indicates that a respective tag is not registered."""

    pass
