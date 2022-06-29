from reportlab.pdfgen.canvas import Canvas

import sys
from PIL import Image
import cv2
from reportlab.lib.units import inch

video_name = sys.argv[1]
vidcap = cv2.VideoCapture(video_name)

width  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)

#100 characters = 7.5in width
new_width = int(sys.argv[2])
new_height = int(new_width * (height/width) * (6/10)) #6/10 accounts for size of font characters

width_in = new_width * (7.5 / 100)
height_in = width_in * (new_height / new_width) * (10/6)

canvas = Canvas("../media/video.pdf", pagesize=(width_in * inch, height_in * inch))

success, image = vidcap.read()
while success:
    img = Image.fromarray(image)
    img = img.resize((new_width, new_height))
    img = img.convert('L')
    pixels = img.getdata()

    # replace each pixel with a character from array
    charsString = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    chars = []
    chars[:0] = charsString
    new_pixels = [chars[round(pixel / 3.75)] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [
        new_pixels[index:index + new_width]
        for index in range(0, new_pixels_count, new_width)
    ]
    ascii_image = "\n".join(ascii_image)

    canvas.setFont("Courier", 9)
    t = canvas.beginText(0 * inch, height_in * inch)
    t.textLines(ascii_image)
    canvas.drawText(t)

    canvas.showPage()
    success, image = vidcap.read()

canvas.save()