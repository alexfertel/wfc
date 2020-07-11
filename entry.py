#!/usr/bin/python3
import argparse
import logging
import os

from pprint import pprint
from pathlib import Path
from src import Interface, Texture, CLASSIFIERS, VALIDATORS, RENDERERS
from src.utils import find
from src.generalization import generalization


def main():
    main_parser = argparse.ArgumentParser(prog="wfc")

    add_flags(main_parser)
    main_parser.add_argument(
        'positive', default=['Colored City'], nargs='+')
    main_parser.add_argument(
        '--negative', default=[], nargs='*')
    main_parser.set_defaults(func=generalization)

    args = main_parser.parse_args()
    args.size = (args.size[0], args.size[1])

    # Create the output dir if it doesn't exist
    Path(os.path.join('results', args.name)).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('results', 'matrices', args.name)).mkdir(
        parents=True, exist_ok=True)

    args.positive = map(lambda pic_name: os.path.join(
        'images', f'{pic_name}.png'), args.positive)
    args.negative = map(lambda pic_name: os.path.join(
        'images', f'{pic_name}.png'), args.negative)

    args.path = os.path.join('images', f'{args.name}.png')

    if not hasattr(args, 'func'):
        main_parser.print_help()
    else:
        args.func(args)


def add_flags(parser):
    parser.add_argument('name', default='Flowers1', help='Image name.')
    parser.add_argument('-s', '--size', nargs=2, type=int, default=(28, 28),
                        help='Tuple representing the size of the output image.',
                        dest='size')
    parser.add_argument('--rotate', action='store_true',
                        help="Allow rotations.", dest='rotate')
    parser.add_argument('--reflect', action='store_true',
                        help="Allow reflection.", dest='reflect')
    parser.add_argument('-c', '--classifier', default='deterministicclassifier',
                        help='Classifier to use.', dest='classifier')
    parser.add_argument('-v', '--validator', default='deterministicvalidator',
                        help='Validator to use.', dest='validator')
    parser.add_argument('-r', '--renderer', default='deterministicrenderer',
                        help='Renderer to use.', dest='renderer')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Don't compute each step.", dest='quiet')
    parser.add_argument('-n', type=int, default=3,
                        help="Size of a pattern side.", dest='N')
    parser.add_argument('--alpha', type=float, default=.0,
                        help='Relaxation parameter.',
                        dest='alpha')



if __name__ == "__main__":
    main()
