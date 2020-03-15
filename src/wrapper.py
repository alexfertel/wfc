import os
import numpy as np
import imageio as im

from src.utils import extract_submatrices as es
from src.utils import extract_wrapped_pattern as ewp
from functools import reduce, partial

from pprint import pprint


def dichotomic(args):
    pprint(args)

    pimages, nimages, c2i, i2c = read_images(args.positive, args.negative)
    psamples = [compute_sample(rgb, c2i) for rgb in pimages]
    nsamples = [compute_sample(rgb, c2i) for rgb in nimages]

    pprint(psamples)

    extractor = partial(es, ewp, args.N)
    transformer = partial(transform, args.rotate, args.reflect)
    
    clf = args.classifier()

    ppatterns = reduce(
        lambda x, y: x + extractor(y), psamples, [])
    
    ppatterns = reduce(
        lambda x, y: x + transformer(y), ppatterns, [])

    punique, pindices, counts = np.lib.arraysetops.unique(
        ppatterns, return_inverse=True, return_counts=True, axis=0)

    pprint(pindices)

    ppatterns = [clf.classify_pattern(pattern) for pattern in punique]
    for index, pattern in enumerate(ppatterns): pattern.count = counts[index]

    npatterns = reduce(
        lambda x, y: x + extractor(y), nsamples, [])
    
    npatterns = reduce(
        lambda x, y: x + transformer(y), npatterns, [])

    nunique = np.lib.arraysetops.unique(
        npatterns, axis=0) if npatterns else []

    pprint(punique)
    pprint(np.concatenate((punique, nunique)))    



def transform(allow_rotations, allow_reflections, pattern):
    patterns = [pattern]
    if allow_rotations or allow_reflections:
        sm = None
        for _ in range(3):
            if allow_rotations:
                sm = np.rot90(pattern)
                patterns.append(sm)

            if allow_reflections:
                sm = np.flip(sm)
                patterns.append(sm)

    return patterns


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


def mergec2i(c2i1, c2i2):
    """
    Merge two color-to-index dicts taking the first one as
    the truth.
    """
    i = 1
    n = len(c2i1.keys())
    for color in c2i2.keys():
        if not color in c2i1.keys():
            c2i2[color] = n + i
            i += 1

    result = {**c2i2, **c2i1}
    return result


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

    return np.array(sample)
