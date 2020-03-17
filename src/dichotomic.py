import os
import numpy as np
import imageio as im

from src.core import Core
from src.utils import extract_submatrices as es
from src.utils import extract_wrapped_pattern as ewp
from functools import reduce, partial

from pprint import pprint


def dichotomic(args):
    pimages, nimages, c2i, i2c = read_images(args.positive, args.negative)
    psamples = [compute_sample(rgb, c2i) for rgb in pimages]
    nsamples = [compute_sample(rgb, c2i) for rgb in nimages]

    pprint(psamples)

    extractor = partial(es, ewp, args.N, args.ground)
    transformer = partial(transform, args.rotate, args.reflect)

    # Classifier setup
    clf = args.classifier()

    ppatterns = reduce(
        lambda x, y: x + extractor(y), psamples, [])

    ppatterns = reduce(
        lambda x, y: x + transformer(y), ppatterns, [])

    punique, pindices, weights = np.lib.arraysetops.unique(
        ppatterns, return_inverse=True, return_counts=True, axis=0)

    ppatterns = [clf.classify_pattern(pattern) for pattern in punique]
    for index, pattern in enumerate(ppatterns):
        pattern.count = weights[index]

    npatterns = reduce(
        lambda x, y: x + extractor(y), nsamples, [])

    npatterns = reduce(
        lambda x, y: x + transformer(y), npatterns, [])

    nunique = np.lib.arraysetops.unique(
        npatterns, axis=0) if npatterns else []

    npatterns = [clf.classify_pattern(pattern) for pattern in nunique]

    # Validator setup
    validator = args.validator()
    validator.learn(ppatterns).prune(npatterns).postprocess(ppatterns)    

    pprint(validator.lt, indent=2, width=200)
    pprint(validator.lt.get_matrix(len(ppatterns)), indent=2, width=200)

    # Renderer setup
    renderer = args.renderer(ppatterns)

    core = Core(ppatterns, weights, validator, args.N)

    grid = generate(core, args.name, args.size, args.quiet, i2c)

    n, m = args.size
    id_grid = [[-1 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            id_grid[i][j] = grid[i][j].identifier

    rendered_grid = renderer.render_patterns(np.array(id_grid))

    pprint(rendered_grid, indent=2, width=200)


def generate(core, name, size, quiet, i2c):
    if quiet:
        for _ in enumerate(core.generate(size)):
            continue
    else:
        for index, grid in enumerate(core.generate(size)):
            print(f'Generated step #{index}.')

            save(grid,
                 f'results/{name}/{name}_{index}.png',
                 i2c,
                 slots_array=True)

    return core.grid


def save(grid, path, i2c, slots_array=False):
    rgb = grid
    if slots_array:
        rgb = compute_wave_colors(grid, i2c)

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


def compute_wave_colors(grid, i2c):
    n, m = len(grid), len(grid[0])

    rgb = [[None for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            red, green, blue = (0, 0, 0)
            contributors = [p for p in grid[i]
                            [j].patterns if grid[i][j].possibilities[p.index]]

            for allowed_pattern in contributors:
                red += i2c[allowed_pattern.color][0]
                green += i2c[allowed_pattern.color][1]
                blue += i2c[allowed_pattern.color][2]

            N = len(contributors)
            rgb[i][j] = (red / N, green / N, blue / N)

    return rgb
