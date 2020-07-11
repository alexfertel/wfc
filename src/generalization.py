from src.core import Core
from src.utils import extract_submatrices as es
from src.utils import extract_wrapped_pattern as ewp
from src.functions.generalization import *
from src.functions.decorators import log
from src.functions import classifiers, validators, renderers
from functools import reduce, partial

from pprint import pprint


@log(logging)
def generalization(args):
    logging.info(f'Entering generalization')
    pimages, nimages, c2i, i2c = read_images(args.positive, args.negative)
    psamples = [compute_sample(rgb, c2i) for rgb in pimages]
    nsamples = [compute_sample(rgb, c2i) for rgb in nimages]

    pprint(psamples)

    extractor = partial(es, ewp, args.N)
    transformer = partial(transform, args.rotate, args.reflect)

    # Classifier setup
    (_, classify) = getattr(classifiers, args.classifier)()

    ppatterns = reduce(
        lambda x, y: x + extractor(y), psamples, [])

    ppatterns = reduce(
        lambda x, y: x + transformer(y), ppatterns, [])

    punique, pindices, weights = np.lib.arraysetops.unique(
        ppatterns, return_inverse=True, return_counts=True, axis=0)

    pprint(punique, indent=2, width=100)
    pprint(pindices, indent=2, width=200)

    ppatterns = [classify(pattern) for pattern in punique]
    for index, pattern in enumerate(ppatterns):
        pattern.count = weights[index]

    npatterns = reduce(
        lambda x, y: x + extractor(y), nsamples, [])

    npatterns = reduce(
        lambda x, y: x + transformer(y), npatterns, [])

    nunique = np.lib.arraysetops.unique(
        npatterns, axis=0) if npatterns else []

    npatterns = [classify(pattern) for pattern in nunique]

    (process, valid) = getattr(validators, args.validator)(args.alpha)
    process(ppatterns, npatterns)

    # pprint(validator.lt, indent=2, width=100)
    # pprint(validator.lt.get_matrix(len(ppatterns)), indent=2, width=200)

    core = Core(ppatterns, weights, valid, args.N)

    grid = generate(core, args.name, args.size, args.quiet, i2c)

    # Renderer setup
    render = getattr(renderers, args.renderer)(ppatterns)

    rendered_grid = render(np.array(grid))

    pprint(rendered_grid, indent=2, width=200)
