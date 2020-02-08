#!/usr/bin/python3
import argparse
import os

from pprint import pprint
from pathlib import Path
from src import Interface, Texture


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
    args = parser.parse_args()
    args.size = (args.size[0], args.size[1])

    # Create the output dir if it doesn't exist
    Path(os.path.join('results', args.name)).mkdir(parents=True, exist_ok=True)

    path = os.path.join('images', f'{args.name}.png')
    wfc = Texture(args.N, path)
    wfc.generate(args.name, args.size)

if __name__ == "__main__":
    main()


