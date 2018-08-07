"""Image related messages."""

from hinews.messages.common import NewsMessage


__all__ = [
    'NoSuchImage',
    'NoImageProvided',
    'NoMetaDataProvided',
    'ImageAdded',
    'ImageDeleted',
    'ImagePatched']


class NoSuchImage(NewsMessage):
    """Indicates that the respective image does not exist."""

    STATUS = 404


class NoImageProvided(NewsMessage):
    """Indicates that no image was provided during POST request."""

    STATUS = 422


class NoMetaDataProvided(NewsMessage):
    """Indicates that no meta data was provided during POST request."""

    STATUS = 422


class ImageAdded(NewsMessage):
    """Indicates that the image was added sucessfully."""

    STATUS = 201


class ImageDeleted(NewsMessage):
    """Indicates tat the image was deleted successfully."""

    STATUS = 200


class ImagePatched(NewsMessage):
    """Indicates that the image was patched successfully."""

    STATUS = 200
