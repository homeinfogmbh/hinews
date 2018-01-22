"""Write watermark text onto images."""

from collections import namedtuple
from functools import partial
from io import BytesIO
from tempfile import TemporaryFile

from PIL import Image, ImageDraw, ImageFont

__all__ = ['watermark']


TTF_DEJAVU = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_SIZE = 12
OFFSET = 10


Size = namedtuple('Size', ('width', 'height'))


def make_watermark(size, text, font):
    """Creates an interim watermark image."""

    image = Image.new('RGBA', size, color=(0, 0, 0, 0))
    # Write text on interim watermark image.
    draw = ImageDraw.Draw(image)
    draw.text((OFFSET, OFFSET), text, fill=(255, 255, 255), font=font)
    # Calculate mask <https://gist.github.com/snay2/876425>.
    mask = image.convert('L').point(partial(max, 100))
    image.putalpha(mask)
    return image


def watermark(image_data, text, font=None):
    """Writes the respective text onto the image."""

    if font is None:
        font = ImageFont.truetype(TTF_DEJAVU, FONT_SIZE)

    image = Image.open(BytesIO(image_data))
    watermark_size = Size(image.width, font.size + 2*OFFSET)
    watermark_position = Size(0, image.height - watermark_size.height)
    watermark_image = make_watermark(watermark_size, text, font)
    image.paste(watermark_image, watermark_position, mask=watermark_image)

    with TemporaryFile('w+b') as tmp:
        image.save(tmp, format=image.format)
        tmp.seek(0)
        return tmp.read()
