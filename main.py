#!/usr/bin/python3
#!/usr/bin/python3
import argparse
import os

from pprint import pprint
from pathlib import Path
from src import Interface, Texture, RENDERERS, VALIDATORS
from src.utils import find


def main():
    # create the top-level parser
    main_parser = argparse.ArgumentParser(prog="wfc")
    subparsers = main_parser.add_subparsers()

    # create the parser for the "simple" command
    simple_parser = subparsers.add_parser('simple')
    simple_parser.add_argument('name', default='Flowers1',
                               help='Sample name.')
    simple_parser.add_argument('-g', '--ground', type=int, default=0,
                               help='The height in pixels of the ground.',
                               dest='ground')
    add_flags(simple_parser)
    simple_parser.set_defaults(func=simple)

    # create the parser for the "dichotomic" command
    dichotomic_parser = subparsers.add_parser('dichotomic')
    dichotomic_parser.add_argument('positive', default=['Colored City'], nargs='+')
    dichotomic_parser.add_argument('negative', default=['Colored City Negative'], nargs='*')
    add_flags(dichotomic_parser)
    dichotomic_parser.set_defaults(func=dichotomic)

    args = main_parser.parse_args()
    args.size = (args.size[0], args.size[1])

    # Create the output dir if it doesn't exist
    Path(os.path.join('results', args.name)).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('results', 'matrices', args.name)).mkdir(
        parents=True, exist_ok=True)

    if args.renderer:
        args.renderer = find(RENDERERS, args.renderer)

    if args.validator:
        args.validator = find(VALIDATORS, args.validator)

    args.path = os.path.join('images', f'{args.name}.png')

    if not hasattr(args, 'func'):
        main_parser.print_help()
    else:
        args.func(args)


def add_flags(parser):
    parser.add_argument('-s', '--size', nargs=2, type=int, default=(28, 28),
                        help='Tuple representing the size of the output image.',
                        dest='size')
    parser.add_argument('--rotate', action='store_true',
                        help="Allow rotations.", dest='rotate')
    parser.add_argument('--reflect', action='store_true',
                        help="Allow reflection.", dest='reflect')
    parser.add_argument('-r', '--renderer', default=None,
                        help='Renderer to use.', dest='renderer')
    parser.add_argument('-v', '--validator', default=None,
                        help='Validator to use.', dest='validator')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Don't compute each step.", dest='quiet')
    parser.add_argument('-n', type=int, default=3,
                        help="Size of a pattern side.", dest='N')

    


def simple(args):
    wfc = Texture(args.path, args.N, ground=args.ground, validator=args.validator,
                  renderer=args.renderer, allow_rotations=args.rotate)

    wfc.generate(args.name, args.size, quiet=args.quiet)

    wfc.render(args.name)


def dichotomic(args):
    pass


if __name__ == "__main__":
    main()
