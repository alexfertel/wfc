#!/usr/bin/python3
import argparse
import os

from pprint import pprint
from pathlib import Path
from src import Interface, Texture, RENDERERS


def main():
    parser = argparse.ArgumentParser()

    default = 'Rooms'
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
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help="Don't compute each step.",
                        dest='quiet')

    args = parser.parse_args()
    args.size = (args.size[0], args.size[1])

    if args.renderer:
        args.renderer = find(RENDERERS, args.renderer)        

    # Create the output dir if it doesn't exist
    Path(os.path.join('results', args.name)).mkdir(parents=True, exist_ok=True)

    path = os.path.join('images', f'{args.name}.png')
    wfc = Texture(args.N, path, renderer=args.renderer)
    wfc.generate(args.name, args.size, quiet=args.quiet)

    wfc.render(args.name)

def find(elements, value):
    value = value.lower()
    for obj in elements:
        if obj.__name__.lower() == value:
            return obj
    raise ValueError(f"{value} not found in {[e.__name__ for e in elements]}")


if __name__ == "__main__":
    main()
