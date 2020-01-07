#!/usr/bin/python3
import argparse
import os

from src.core import Core
from src.graphics import Texture
from pprint import pprint

def main():
    parser = argparse.ArgumentParser()

    default = 'Flowers'
    parser.add_argument('--name', 
                        default=default,
                        help='Output name.', 
                        dest='name')
    parser.add_argument('-i', '--image', 
                        default=os.path.join('images', f'{default}.png'),
                        help='Path to the example image.', 
                        dest='path')
    parser.add_argument('-n', type=int, 
                        default=3,
                        help="Size of the patterns' side.",
                        dest='N')
    parser.add_argument('--size', nargs=2,
                        type=lambda args: (int(args[0]), int(args[1])),
                        default=(28, 28),
                        help='Tuple representing the size of the output image.',
                        dest='size')
    parser.add_argument('-o', '--output-dir',
                        default=os.path.join('results', default, ''),
                        help='Tuple representing the size of the output image.',
                        dest='opath')
    args = parser.parse_args()
    
    generate(args.name,
             args.path, 
             args.N, 
             args.size,
             args.opath)


    
def generate(name, path, N, size, opath):
    tex = Texture(path)

    sample = tex.sample

    wfc = Core(sample, N)

    for index, grid in enumerate(wfc.generate(size)):
        print(f'Generated step #{index}.')
        tex.save(grid, os.path.join(opath, f"{name}{index}.bmp"))

        # pprint(grid, width=200)

if __name__ == "__main__":
    main()


