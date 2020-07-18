from wfc.extraction import extract_submatrices as es, extract_patterns
from wfc.extraction import extract_wrapped_pattern as ewp
from wfc.extraction import transform_patterns, transform
from wfc.core import wfc
from wfc.image_handling import *
from wfc import validators, renderers, classifiers
from functools import partial


def concat(items):
    return reduce(lambda a, b: a + b, items, [])


def generalization(args):
    pimages, nimages, c2i, i2c = read_images(args.positive, args.negative)

    psamples = [compute_sample(rgb, c2i) for rgb in pimages]
    nsamples = [compute_sample(rgb, c2i) for rgb in nimages]

    extractor = partial(es, ewp, args.N)
    transformer = partial(transform, args.rotate, args.reflect)

    epsamples = extract_patterns(psamples, extractor)
    ensamples = extract_patterns(nsamples, extractor)

    # distance_table = measure(epsamples)

    ppatterns = concat(epsamples)
    npatterns = concat(ensamples)

    ppatterns = transform_patterns(ppatterns, transformer)
    npatterns = transform_patterns(npatterns, transformer)

    (classify, pclassified) = getattr(classifiers, args.classifier)(ppatterns)

    nunique = np.lib.arraysetops.unique(
        npatterns, axis=0) if npatterns else []

    nclassified = [classify(pattern) for pattern in nunique]

    (process, valid, *_) = getattr(validators, args.validator)(args.alpha, args.delta)
    process(pclassified, nclassified)

    grid, generate = wfc(pclassified, valid, args.size)

    run(generate, args.name, args.quiet, i2c, pclassified)

    (render, *_) = getattr(renderers, args.renderer)(pclassified)

    rendered_grid = render(grid)

    return rendered_grid
