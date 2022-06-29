import sys
from PIL import Image
import cv2
import time
import os

video_name = sys.argv[1]
if (video_name == "camera"):
    video_name = 1
vidcap = cv2.VideoCapture(video_name)

startTime = time.time()
nextTime = 1 / vidcap.get(cv2.CAP_PROP_FPS)

size = os.get_terminal_size()
new_width = size.columns
new_height = size.lines + 2 #add 2 because terminal is weird

success,image = vidcap.read()
while success:
    img = Image.fromarray(image)
    img = img.resize((new_width, new_height))
    img = img.convert('L')
    pixels = img.getdata()

    # replace each pixel with a character from array
    charsString = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    chars = []
    chars[:0] = charsString
    new_pixels = [chars[round(pixel/3.75)] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    while (time.time() - startTime) < nextTime:
        pass
    nextTime += 1 / vidcap.get(cv2.CAP_PROP_FPS)

    print(ascii_image)
    success,image = vidcap.read()