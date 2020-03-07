#!/usr/bin/python3
#!/usr/bin/python3
import argparse
import os

from pprint import pprint
from pathlib import Path
from src import Interface, Texture, RENDERERS, VALIDATORS
from src.utils import find

def main():
    parser = argparse.ArgumentParser()

    default = 'Flowers1'
    parser.add_argument('--name',
                        default=default,
                        help='Sample name.',
                        dest='name')
    parser.add_argument('-i', '--image',
                        default=os.path.join('images', f'{default}.png'),
                        help='Path to the example image.',
                        dest='path')
    parser.add_argument('-n', type=int,
                        default=3,
                        help="Size of the patterns' side.",
                        dest='N')
    parser.add_argument('-s', '--size', nargs=2,
                        type=int,
                        default=(28, 28),
                        help='Tuple representing the size of the output image.',
                        dest='size')
    parser.add_argument('-r', '--renderer',
                        default=None,
                        help='Renderer to use.',
                        dest='renderer')
    parser.add_argument('-v', '--validator',
                        default=None,
                        help='Validator to use.',
                        dest='validator')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help="Don't compute each step.",
                        dest='quiet')
    parser.add_argument('--rotate',
                        action='store_true',
                        help="Allow rotations.",
                        dest='rotate')
    parser.add_argument('--all-renderers',
                        action='store_true',
                        help="Test all of scikit-learn models.",
                        dest='all')
    parser.add_argument('-t',
                        action='store_true',
                        help="With timestamp.",
                        dest='timestamp')



    args = parser.parse_args()
    args.size = (args.size[0], args.size[1])

    # Create the output dir if it doesn't exist
    Path(os.path.join('results', args.name)).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('results', 'matrices', args.name)).mkdir(parents=True, exist_ok=True)
    
    if args.all:
        every(args)
        exit()
    
    one(args)

def every(args):
    pass

def one(args):
    if args.renderer:
        args.renderer = find(RENDERERS, args.renderer)        

    if args.validator:
        args.validator = find(VALIDATORS, args.validator)        

    # filename = 

    path = os.path.join('images', f'{args.name}.png')
    wfc = Texture(args.N, path, validator=args.validator, renderer=args.renderer, allow_rotations=args.rotate)
    wfc.generate(args.name, args.size, quiet=args.quiet)

    wfc.render(args.name)


if __name__ == "__main__":
    main()
