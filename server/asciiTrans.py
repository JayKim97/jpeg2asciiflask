try:
    from PIL import Image
except ImportError:
    import Image
import PIL
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw
import cv2
import numpy as np
PIL.Image.MAX_IMAGE_PIXELS = 933120000
PIXEL_ON = 0
PIXEL_OFF = 255


def asciiTran(filename):
    scaledImage = scaleImage("./static/uploads/"+filename)
    textifed = textifyImage(scaledImage)
    resImage = text_image(textifed)
    print("HERE")
    resImage.save("./static/results/result.png")


def simple(i):
    c = ""
    if i > 225:
        c = " "
    elif i > 200:
        c = "."
    elif i > 175:
        c = ":"
    elif i > 150:
        c = "-"
    elif i > 125:
        c = "="
    elif i > 100:
        c = "+"
    elif i > 75:
        c = "*"
    elif i > 50:
        c = "#"
    elif i > 25:
        c = "%"
    else:
        c = "@"

    return c


def scaleImage(imgName):
    img = cv2.imread(imgName)
    # image to gray
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rate = 100
    # get image size
    height, width, channels = img.shape
    if(height > rate or width > rate):
        if(height > width):
            scale_percent = rate/height
        else:
            scale_percent = rate / width
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)

    img_gray = cv2.resize(img_gray, dim, interpolation=cv2.INTER_AREA)
    return img_gray


def textifyImage(image):
    width = int(image.shape[1])
    height = int(image.shape[0])
    imageText = ""

    pixelmap = [[0]*width for i in range(height)]
    for i in range(height):
        for j in range(width):
            pixelmap[i][j] = int(image[i, j])-30

    charMap = [[" "]*width for i in range(height)]
    for i in range(height):
        for j in range(width):
            charMap[i][j] = simple(pixelmap[i][j])
    for i in range(height):
        for j in range(width):
            imageText += charMap[i][j]+" "
        imageText += "\n"
    return imageText


def text_image(text):
    lines = tuple(l.rstrip() for l in text.splitlines())
    large_font = 10
    font_path = "Cousine-Regular.ttf"
    grayscale = 'L'
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
        print("worked")
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # convert points to pixels
    def pt2px(pt): return int(round(pt * 96.0 / 72))
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    # crop the text
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    print("HEREE")
    return image
