"""Write watermark text onto images."""

from functools import partial
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


__all__ = ['watermark']


TTF_DEJAVU = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_SIZE = 12
DEFAULT_FONT = ImageFont.truetype(TTF_DEJAVU, FONT_SIZE)
OFFSET = 10


def write_text(image, text, font):
    """Writes the text onto the respective image."""

    position = (OFFSET, OFFSET)
    fill = (255, 255, 255)
    ImageDraw.Draw(image).text(position, text, fill=fill, font=font)


def make_watermark(size, text, font, color=(0, 0, 0, 0), mode='RGBA'):
    """Creates an interim watermark image."""

    image = Image.new(mode, size, color=color)
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


def watermark(image_data, text, font=DEFAULT_FONT):
    """Writes the respective text onto the image."""

    image = Image.open(BytesIO(image_data))
    watermark_size = (image.width, font.size + 2*OFFSET)
    watermark_position = (0, image.height - watermark_size[1])
    watermark_image = make_watermark(watermark_size, text, font)
    image.paste(watermark_image, watermark_position, mask=watermark_image)
    return dump(image)
