#!/usr/bin/python3
import sys
import imageio as im
import glob

# if len(sys.argv) != 4:
#     print(
#         "Usage: python swapper.py path/to/image path/to/output scale_factor \nExample: python swapper.py "
#         "../images/Flowers1.png ../images/Flowers2.png 2")
#     exit()

filenames = glob.glob(sys.argv[1] + '*')  # Get all the files in the directory
output_path = '../scaled/'
factor = int(sys.argv[2]) if len(sys.argv) > 2 else 32

print(filenames)

for filename in filenames:
    read_image = im.imread(filename)
    new_image = read_image.repeat(factor, axis=0).repeat(factor, axis=1)
    im.imwrite(output_path + filename.split('/')[-1], new_image)

