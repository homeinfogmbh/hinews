"""Write watermark text onto images."""

from collections import namedtuple
from functools import partial
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

__all__ = ['watermark']


TTF_DEJAVU = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_SIZE = 12
OFFSET = 10


Size = namedtuple('Size', ('width', 'height'))


def write_text(image, text, font):
    """Writes the text onto the respective image."""

    position = (OFFSET, OFFSET)
    fill = (255, 255, 255)
    ImageDraw.Draw(image).text(position, text, fill=fill, font=font)


def make_watermark(size, text, font):
    """Creates an interim watermark image."""

    color = (0, 0, 0, 0)
    image = Image.new('RGBA', size, color=color)
    write_text(image, text, font)
    # Calculate mask <https://gist.github.com/snay2/876425>.
    mask = image.convert('L').point(partial(max, 100))
    image.putalpha(mask)
    return image


def dump(image):
    """Dumps the image into the respective format."""

    buf = BytesIO()
    image.save(buf, format=image.format)
    buf.flush()
    buf.seek(0)
    return buf.read()


def watermark(image_data, text, font=None):
    """Writes the respective text onto the image."""

    if font is None:
        font = ImageFont.truetype(TTF_DEJAVU, FONT_SIZE)

    image = Image.open(BytesIO(image_data))
    watermark_size = Size(image.width, font.size + 2*OFFSET)
    watermark_position = Size(0, image.height - watermark_size.height)
    watermark_image = make_watermark(watermark_size, text, font)
    image.paste(watermark_image, watermark_position, mask=watermark_image)
    return dump(image)
