from src.utils import extract_submatrices as es
from src.utils import extract_wrapped_pattern as ewp
from src.functions.core import wfc
from src.functions.generalization import *
from src.functions.decorators import log
from src.functions import classifiers, validators, renderers
from functools import reduce, partial

from pprint import pprint


def extract_patterns(samples, extractor):
    return reduce(lambda x, y: x + extractor(y), samples, [])


def transform_patterns(patterns, transformer):
    return reduce(lambda x, y: x + transformer(y), patterns, [])


@log(logging)
def generalization(args):
    pimages, nimages, c2i, i2c = read_images(args.positive, args.negative)
    psamples = [compute_sample(rgb, c2i) for rgb in pimages]
    nsamples = [compute_sample(rgb, c2i) for rgb in nimages]

    pprint(psamples)

    extractor = partial(es, ewp, args.N)
    transformer = partial(transform, args.rotate, args.reflect)

    ppatterns = extract_patterns(psamples, extractor)
    npatterns = extract_patterns(nsamples, extractor)

    ppatterns = transform_patterns(ppatterns, transformer)
    npatterns = transform_patterns(npatterns, transformer)

    punique, pindices, weights = np.lib.arraysetops.unique(
        ppatterns, return_inverse=True, return_counts=True, axis=0)

    nunique = np.lib.arraysetops.unique(
        npatterns, axis=0) if npatterns else []

    pprint(punique, indent=2, width=100)
    pprint(pindices, indent=2, width=200)

    (classify, *_) = getattr(classifiers, args.classifier)()

    ppatterns = [classify(pattern) for pattern in punique]
    npatterns = [classify(pattern) for pattern in nunique]

    for index, pattern in enumerate(ppatterns):
        pattern.count = weights[index]

    (process, valid, *_) = getattr(validators, args.validator)(args.alpha)
    process(ppatterns, npatterns)

    grid, generate = wfc(ppatterns, valid, args.size)

    run(generate, args.name, args.quiet, i2c)

    (render, *_) = getattr(renderers, args.renderer)(ppatterns)

    rendered_grid = render(np.array(grid))

    pprint(rendered_grid, indent=2, width=200)
