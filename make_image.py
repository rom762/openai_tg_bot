import logging

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
import os


def get_image_filename(first_text: str, second_text: str) -> str:
    template_fn = os.path.join(os.getcwd(), 'images', 'cats.jpg')
    ttf = os.path.join(os.getcwd(), 'fonts', 'comic.ttf')
    if not os.path.exists(template_fn):
        logging.error("Can't find template image for making mem")
    if not os.path.exists(ttf):
        logging.error("Can't find ttf file for font for making mem")

    img = Image.open(template_fn)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(ttf, 16)
    draw.text((245, 150), first_text, (255, 255, 255), font=font)
    draw.text((30, 360), f"{second_text}?", (255, 255, 255), font=font)
    draw.text((245, 360), f"{second_text}", (255, 255, 255), font=font)

    output_filename = os.path.join(os.getcwd(), 'images', f"{datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')}_output.jpg")
    img.save(output_filename)
    return output_filename


if __name__ == '__main__':
    filename = get_image_filename('Sample text', 'And one more')
    print(f"filename: {filename}")
    if filename:
        image = Image.open(filename)
        image.show()
