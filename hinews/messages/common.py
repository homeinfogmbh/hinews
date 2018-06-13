"""Messages."""

from his import Message

__all__ = ['NewsMessage']


class NewsMessage(Message):
    """A JSON-ish response."""

    LOCALES = '/etc/his.d/locale/hinews.ini'
