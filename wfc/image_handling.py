import numpy as np
import imageio as im

from functools import reduce
from time import time


def run(generate, name, quiet, i2c, patterns):
    grid, wave = None, None

    if quiet:
        *_, last = generate()
        grid, wave = last
    else:
        generator = generate()
        index = 1
        while True:
            try:
                print(f'Generated step #{index}.')
                grid, wave = next(generator)

                save(grid,
                     wave,
                     f'results/{name}/{name}_{index}.png',
                     i2c, patterns)
                index += 1

            except StopIteration:
                break

    timestamp = ''.join(str(time()).split('.'))
    save(grid,
         wave,
         f'results/{name}/{name}_{timestamp}.png',
         i2c, patterns)
    print('Finished.')


def save(grid, wave, path, i2c, patterns):
    rgb = compute_wave_colors(grid, wave, i2c, patterns)

    data = np.uint8(rgb)
    im.imwrite(path, data)


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

    # print(f'i2c {i2c}')

    return pimages, nimages, c2i, i2c


def mergec2i(c2i1, c2i2):
    """
    Merge two color-to-index dicts taking the first one as
    the truth.
    """
    i = 1
    n = len(c2i1.keys())
    for color in c2i2.keys():
        if color not in c2i1.keys():
            c2i2[color] = n + i
            i += 1

    result = {**c2i2, **c2i1}
    return result


def get_color_map(image):
    n, m, _ = image.shape
    colors = []
    for i in range(n):
        for j in range(m):
            colors.append(image[i][j])

    colors = np.lib.arraysetops.unique(colors, axis=0)
    # print(colors)
    c2i = {tuple(color): index for index, color in enumerate(colors)}

    return c2i


def compute_sample(rgb, c2i):
    n, m, _ = rgb.shape

    sample = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            sample[i][j] = c2i[tuple(rgb[i][j])]

    return np.array(sample)


def compute_wave_colors(grid, wave, i2c, patterns):
    n, m = grid.shape

    rgb = [[None for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            red, green, blue = (0, 0, 0)
            contributors = [identifier for identifier, is_possible in enumerate(wave[i][j]) if is_possible]

            for c in contributors:
                red += i2c[patterns[c].color][0]
                green += i2c[patterns[c].color][1]
                blue += i2c[patterns[c].color][2]

            clen = len(contributors)
            rgb[i][j] = (red / clen, green / clen, blue / clen)

    return rgb
