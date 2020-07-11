import numpy as np

from src.functions.generalization import *
from src.core import Core
from src.utils import extract_submatrices as es
from src.utils import extract_wrapped_pattern as ewp
from functools import reduce, partial

from pprint import pprint


def generalization(args):
    pimages, nimages, c2i, i2c = read_images(args.positive, args.negative)
    psamples = [compute_sample(rgb, c2i) for rgb in pimages]
    nsamples = [compute_sample(rgb, c2i) for rgb in nimages]

    pprint(psamples)

    extractor = partial(es, ewp, args.N)
    transformer = partial(transform, args.rotate, args.reflect)

    # Classifier setup
    clf = args.classifier()

    ppatterns = reduce(
        lambda x, y: x + extractor(y), psamples, [])

    ppatterns = reduce(
        lambda x, y: x + transformer(y), ppatterns, [])

    punique, pindices, weights = np.lib.arraysetops.unique(
        ppatterns, return_inverse=True, return_counts=True, axis=0)

    pprint(punique, indent=2, width=100)
    pprint(pindices, indent=2, width=200)

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
    validator = args.validator(args.alpha)
    validator.learn(ppatterns).prune(npatterns).postprocess(ppatterns)

    # pprint(validator.lt, indent=2, width=100)
    # pprint(validator.lt.get_matrix(len(ppatterns)), indent=2, width=200)

    core = Core(ppatterns, weights, validator, args.N)

    grid = generate(core, args.name, args.size, args.quiet, i2c)

    n, m = args.size
    id_grid = [[-1 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            id_grid[i][j] = grid[i][j].identifier

    # Renderer setup
    renderer = args.renderer(ppatterns)

    rendered_grid = renderer.render_patterns(np.array(id_grid))

    pprint(rendered_grid, indent=2, width=200)
