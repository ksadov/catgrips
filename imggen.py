from PIL import Image, ImageDraw, ImageFont
import random

TOP_OFFSET = 10
BOTTOM_OFFSET = 20
MEMEWIDTH = 600

"""
This script uses a local folder catpics/ containing 1005 cat images that I
downloaded from kaggle. You can get the data yourself here:
https://www.kaggle.com/c/dogs-vs-cats/overview
"""

"""Returns a string containing the filename of a random cat image.
"""
def get_cat_img():
    r = random.randrange(1005)
    return f"catpics/{r}.jpg"

"""Returns the position to place meme text.

Attributes:
    draw (ImageDraw.draw): the drawing context p
    text (str): the text to paste
    font (ImageFont.truetype): the font of txt
    toptext (bool): true if the text is toptext, false if bottomtext
"""
def position_text(draw, img, text, font, toptext):
    textwidth, textheight = draw.textsize(text, font = font)
    imgwidth, imgheight = img.size
    if (toptext):
        ypos = TOP_OFFSET
    else:
        ypos = imgheight - (BOTTOM_OFFSET + textheight)
    return ((imgwidth - textwidth)/2, ypos)

"""Returns two random lines from a file of lyrics.

Attributes:
    fname (str): the name of the lyrics file
"""
def get_text(fname):
    toptext = None
    bottomtext = None
    with open(fname) as f:
        lines = f.read().splitlines()
    while (toptext is None or bottomtext is None
           or (toptext == '' and bottomtext == '')
           or len(toptext) > 30 or len(bottomtext) > 30):
        linenum = random.randrange(len(lines) - 1)
        toptext = lines[linenum].upper()
        bottomtext = lines[linenum+1].upper()
    return toptext, bottomtext

"""Generates an image of a cat picture with Death Grips lyrics.

Attributes:
    fname (str): the filename to store the image in.
"""
def make_meme(fname):
    # get an image
    base = Image.open(get_cat_img()).convert('RGBA')
    #resize
    newheight = MEMEWIDTH * base.height // base.size[0]
    base = base.resize((MEMEWIDTH, newheight))

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype('impact.ttf', 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # get text
    t1, t2 = get_text("lyrics.txt")
    # draw top text
    w1, h1 = position_text(d, txt, t1, fnt, True)
    d.text((w1,h1), t1, font=fnt, fill=(255,255,255,255),
         stroke_width = 3, stroke_fill = (0, 0, 0, 255))
    # draw bottom text
    w2, h2 = position_text(d, txt, t2, fnt, False)
    d.text((w2,h2), t2, font=fnt, fill=(255,255,255,255),
         stroke_width = 3, stroke_fill = (0, 0, 0, 255))

    out = Image.alpha_composite(base, txt)

    out.save(fname, format = 'PNG')
