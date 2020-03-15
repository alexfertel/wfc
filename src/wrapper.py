import os
import numpy as np
import imageio as im

from src.image_funcs import *
from functools import reduce

from pprint import pprint


def dichotomic(args):
    pprint(args)
    pimages, nimages, c2i, i2c = read_images(args.positive, args.negative)
    psamples = [compute_sample(rgb, c2i) for rgb in pimages]
    nsamples = [compute_sample(rgb, c2i) for rgb in nimages]
    
    pprint(psamples)

    # clf = args.classifier()


def read_images(positive, negative):
    pimages = [im.imread(path) for path in positive]
    pcolors = [get_color_map(image) for image in pimages]

    nimages = [im.imread(path) for path in negative]
    ncolors = [get_color_map(image) for image in nimages]

    c2i = reduce(mergec2i, pcolors + ncolors, {})
    i2c = {v: k for k, v in c2i.items()}
    
    pprint("color2index:")
    pprint(c2i)

    return pimages, nimages, c2i, i2c


def get_color_map(image):
    N, M, _ = image.shape
    colors = []
    for i in range(N):
        for j in range(M):
            colors.append(image[i][j])

    colors = np.lib.arraysetops.unique(colors, axis=0)
    # print(colors)
    c2i = {tuple(color): index for index, color in enumerate(colors)}

    return c2i


def compute_sample(rgb, c2i):
    N, M, _ = rgb.shape

    sample = [[0 for _ in range(M)] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            sample[i][j] = c2i[tuple(rgb[i][j])]

    return sample