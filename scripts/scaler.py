#!/usr/bin/python3
import sys
import imageio as im
import numpy as np

if len(sys.argv) != 4:
    print(
        "Usage: python swapper.py path/to/image path/to/output scale_factor \nExample: python swapper.py "
        "../images/Flowers1.png ../images/Flowers2.png 2")
    exit()

print(sys.argv)

image_path = sys.argv[1]
output_path = sys.argv[2]
factor = int(sys.argv[3])
read_image = im.imread(image_path)

print(read_image)

new_image = read_image.repeat(factor, axis=0).repeat(factor, axis=1)

print(new_image)

im.imwrite(output_path, new_image)
