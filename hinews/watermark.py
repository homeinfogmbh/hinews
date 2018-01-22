"""Write watermark text onto images."""

from io import BytesIO
from tempfile import TemporaryFile

from PIL import Image, ImageDraw, ImageFont

__all__ = [
    'TTF_DEJAVU',
    'YELLOW',
    'top_left',
    'bottom_left',
    'watermark']


TTF_DEJAVU = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
YELLOW = (255, 255, 0)
GREY = (102, 102, 102)


def top_left(_, __, offset=10):
    """Bottom left position in image."""

    return (offset, offset)


def bottom_left(image, font, offset=10):
    """Bottom left position in image."""

    return (offset, image.height - font.size - offset)


def watermark(image_data, text, position=bottom_left, color=GREY, font=None):
    """Writes the respective text onto the image."""

    if font is None:
        font = ImageFont.truetype(TTF_DEJAVU, 25)

    image = Image.open(BytesIO(image_data))
    draw = ImageDraw.Draw(image)
    draw.text(position(image, font), text, fill=color, font=font)

    with TemporaryFile('w+b') as tmp:
        image.save(tmp, format=image.format)
        tmp.seek(0)
        return tmp.read()
