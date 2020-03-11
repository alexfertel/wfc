#!/usr/bin/python3
import imageio
import sys
import glob

if len(sys.argv) != 3:
    print("Usage: python gifmaker.py path/to/directory path/to/output \nExample: python gifmaker.py ../results/Rooms/ ../gifs/rooms.gif")
    exit()

print(sys.argv)

filenames = glob.glob(sys.argv[1] + '*') # Get all the files in the current directory

for name in filenames.copy():
    if not '_' in name:
        filenames.remove(name)

# print(filenames)
list.sort(filenames, key=lambda x: int(x.split('_')[-1].split('.')[0])) # Sort the images by #, this may need to be tweaked for your use case

print(filenames)

images = []
for filename in filenames:
    images.append(imageio.imread(filename))

imageio.mimwrite(sys.argv[2], images, fps=24)
