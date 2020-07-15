from wfc.utils import extract_submatrices as es, extract_patterns, transform_patterns
from wfc.utils import extract_wrapped_pattern as ewp
from wfc.core import wfc
from wfc.image_handling import *
from wfc.decorators import log
from wfc import validators, renderers, classifiers
from functools import partial

from pprint import pprint


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

    run(generate, args.name, args.quiet, i2c, ppatterns)

    (render, *_) = getattr(renderers, args.renderer)(ppatterns)

    rendered_grid = render(grid)

    pprint(rendered_grid, indent=2, width=200)
