"""Write copyright text onto images."""

from io import BytesIO
from tempfile import NamedTemporaryFile

from PIL import Image, ImageDraw, ImageFont

__all__ = ['TTF_DEJAVU', 'top_left', 'bottom_left', 'write_image']


TTF_DEJAVU = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def top_left(_, __):
    """Bottom left position in image."""
    return (0, 0)


def bottom_left(image, font):
    """Bottom left position in image."""
    return (0, image.height - font.size)


def write_image(image_data, text, position=bottom_left, font=None,
                color=(255, 255, 0), suffix='.png'):
    """Writes the respective text onto the image."""

    if font is None:
        font = ImageFont.truetype(TTF_DEJAVU, 25)

    image = Image.open(BytesIO(image_data))
    draw = ImageDraw.Draw(image)
    draw.text(position(image, font), text, color, font=font)
    draw = ImageDraw.Draw(image)

    with NamedTemporaryFile('w+b', suffix=suffix) as tmp:
        image.save(tmp)
        tmp.seek(0)
        return tmp.read()
