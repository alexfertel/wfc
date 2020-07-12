import numpy as np
import imageio as im
import logging

from functools import reduce
from wfc.decorators import log


@log(logging)
def run(generate, name, quiet, i2c):
    if quiet:
        *_, grid = generate()

        save(grid,
             f'results/{name}/{name}.png',
             i2c,
             slots_array=True)
    else:
        for index, step in enumerate(generate()):
            print(f'Generated step #{index}.')

            save(step,
                 f'results/{name}/{name}_{index}.png',
                 i2c,
                 slots_array=True)


@log(logging)
def save(grid, path, i2c, slots_array=False):
    rgb = grid
    if slots_array:
        rgb = compute_wave_colors(grid, i2c)

    data = np.uint8(rgb)
    im.imwrite(path, data)


@log(logging)
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


@log(logging)
def read_images(positive, negative):
    pimages = [im.imread(path) for path in positive]
    pcolors = [get_color_map(image) for image in pimages]

    nimages = [im.imread(path) for path in negative]
    ncolors = [get_color_map(image) for image in nimages]

    c2i = reduce(mergec2i, pcolors + ncolors, {})
    i2c = {v: k for k, v in c2i.items()}

    return pimages, nimages, c2i, i2c


@log(logging)
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


@log(logging)
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


@log(logging)
def compute_sample(rgb, c2i):
    n, m, _ = rgb.shape

    sample = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            sample[i][j] = c2i[tuple(rgb[i][j])]

    return np.array(sample)


@log(logging)
def compute_wave_colors(grid, i2c):
    n, m = len(grid), len(grid[0])

    rgb = [[None for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            red, green, blue = (0, 0, 0)
            contributors = [p for p in grid[i][j].patterns if grid[i][j].possibilities[p.index]]

            for allowed_pattern in contributors:
                red += i2c[allowed_pattern.color][0]
                green += i2c[allowed_pattern.color][1]
                blue += i2c[allowed_pattern.color][2]

            clen = len(contributors)
            rgb[i][j] = (red / clen, green / clen, blue / clen)

    return rgb