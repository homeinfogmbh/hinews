"""Write watermark text onto images."""

from functools import partial
from io import BytesIO
from tempfile import TemporaryFile

from PIL import Image, ImageDraw, ImageFont

__all__ = ['watermark']


TTF_DEJAVU = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_SIZE = 10
OFFSET = 10


def bottom_left(image, font):
    """Bottom left position in image."""

    return (0, image.height - font.size - 2*OFFSET)


def watermark(image_data, text, font=None):
    """Writes the respective text onto the image."""

    # Set default font.
    if font is None:
        font = ImageFont.truetype(TTF_DEJAVU, FONT_SIZE)

    image = Image.open(BytesIO(image_data))
    # Create interim watermark image.
    wmark = Image.new(
        'RGBA', (image.width, font.size + 2*OFFSET), color=(0, 0, 0, 0))
    # Write text on interim watermark image.
    draw = ImageDraw.Draw(wmark)
    draw.text((OFFSET, OFFSET), text, fill=(255, 255, 255), font=font)
    del draw
    # Calculate mask <https://gist.github.com/snay2/876425>.
    mask = wmark.convert('L').point(partial(max, 100))
    wmark.putalpha(mask)
    # Paste interim watermark image into original image.
    image.paste(wmark, bottom_left(image, font), mask=wmark)

    # Return new image data.
    with TemporaryFile('w+b') as tmp:
        image.save(tmp, format=image.format)
        tmp.seek(0)
        return tmp.read()
