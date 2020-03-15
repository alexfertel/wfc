from src.image_funcs import *
from functools import reduce

def dichotomic(args):
    positive, negative, c2i, i2c = read_images(args.positive, args.negative)

    setup_classifier(args.classifier)

def read_images(positive, negative):
    c2i = {}
    psamples = []
    for path in positive:
        sample, color2index = read(path)
        c2i, i2c = mergec2i(c2i, color2index)
        psamples.append(sample)

    nsamples = []
    for path in negative:
        sample, color2index = read(path)
        c2i, i2c = mergec2i(c2i, color2index)
        nsamples.append(sample)

    return psamples, nsamples, c2i, i2c


