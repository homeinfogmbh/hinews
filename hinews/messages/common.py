"""Messages."""

from his import locales, Message

__all__ = ['NewsMessage']


class NewsMessage(Message):
    """A JSON-ish response."""

    LOCALES = locales('/etc/his.d/locale/hinews.ini')
    ABSTRACT = True
