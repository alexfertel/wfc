from wfc.extraction import extract_submatrices as es, extract_patterns, measure
from wfc.extraction import extract_wrapped_pattern as ewp
from wfc.extraction import transform_patterns, transform
from wfc.core import wfc
from wfc.image_handling import *
from wfc import validators, renderers, classifiers
from functools import partial


def concat(items):
    return reduce(lambda a, b: a + b, items, [])


def unique(patterns):
    result = []
    for pattern in patterns:
        if pattern not in result:
            result.append(pattern)

    return result


def generalization(args):
    pimages, nimages, c2i, i2c = read_images(args.positive, args.negative)

    psamples = [compute_sample(rgb, c2i) for rgb in pimages]
    nsamples = [compute_sample(rgb, c2i) for rgb in nimages]

    print("Computed Samples")

    extractor = partial(es, ewp, args.N)
    transformer = partial(transform, args.rotate, args.reflect)

    epsamples = extract_patterns(psamples, extractor)
    ensamples = extract_patterns(nsamples, extractor)

    print("Extracted Patterns")

    ppatterns = concat(epsamples)
    npatterns = concat(ensamples)

    ppatterns = transform_patterns(ppatterns, transformer)
    npatterns = transform_patterns(npatterns, transformer)

    print("Transformed Patterns")

    distance_table = measure(ppatterns, psamples, args.delta)

    (classify, pclassified, *_) = getattr(classifiers, args.classifier)(ppatterns)

    print("Classified Patterns")

    nunique = unique(npatterns)

    nclassified = [classify(pattern) for pattern in nunique]

    (process, valid, *_) = getattr(validators, args.validator)(args.alpha, distance_table)
    process(pclassified, nclassified)

    print("Built Lookup Table")

    grid, generate = wfc(pclassified, valid, args.size)

    print("Initialized Core")

    run(generate, args.name, args.quiet, i2c, pclassified)

    print("Generated Output")

    (render, *_) = getattr(renderers, args.renderer)(pclassified)

    rendered_grid = render(grid)

    print("Rendered Output")

    return rendered_grid
