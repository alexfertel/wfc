import os
import numpy as np
import imageio as im

from .interface import Interface
from PIL import Image
from pprint import pprint


class Texture(Interface):
    def __init__(self,
                 size,
                 path,
                 classifier=None,
                 validator=None,
                 renderer=None,
                 allow_rotations=False,
                 allow_reflections=False):

        # `sample` is an array of arrays that holds the index values for colors
        # as found in the source image.
        self.sample = self.read(path)

        # `colors` is the list of colors that are found in the source image.
        self.colors = {}

        super().__init__(self.sample,
                         size,
                         classifier,
                         validator,
                         renderer,
                         allow_rotations=False,
                         allow_reflections=False)

        # pprint(self.sample)
        # pprint(self.colors)

    def read(self, path):
        image = im.imread(path)
        N, M, _ = image.shape

        colors = []
        for i in range(N):
            for j in range(M):
                colors.append(image[i][j])

        colors = np.lib.arraysetops.unique(colors, axis=0)
        # print(colors)
        self.c2i = {tuple(color): index for index, color in enumerate(colors)}
        self.i2c = {index: tuple(color) for index, color in enumerate(colors)}

        sample = [[0 for _ in range(M)] for _ in range(N)]
        for i in range(N):
            for j in range(M):
                sample[i][j] = self.c2i[tuple(image[i][j])]

        print('Sample:')
        pprint(sample)

        return sample

    def generate(self, name, size, quiet):
        if quiet:
            for _ in enumerate(self.core.generate(size)):
                continue
        else:
            for index, grid in enumerate(self.core.generate(size)):
                print(f'Generated step #{index}.')

                self.save(grid, os.path.join(
                    'results', name, f"{name}_{index}.png"), slots_array=True)

        super().save(self.core.grid, os.path.join(
            'results', 'matrices', name, f"{name}.txt"))

        return self.core.grid

    def save(self, grid, path, slots_array=False):
        rgb = grid
        if slots_array:
            rgb = self.compute_wave_colors(grid)

        data = np.uint8(rgb)
        im.imwrite(path, data)

    def compute_wave_colors(self, grid):
        n, m = len(grid), len(grid[0])

        rgb = [[None for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                red, green, blue = (0, 0, 0)
                contributors = [p for p in grid[i]
                                [j].patterns if grid[i][j].possibilities[p.index]]

                for allowed_pattern in contributors:
                    red += self.i2c[allowed_pattern.color][0]
                    green += self.i2c[allowed_pattern.color][1]
                    blue += self.i2c[allowed_pattern.color][2]

                N = len(contributors)
                rgb[i][j] = (red / N, green / N, blue / N)

        return rgb

    def render(self, name):
        self.save(self.core.grid, os.path.join(
            'results', name, f"{name}.png"), slots_array=True)

        rendered_ids = super().render(name)

        n, m = len(rendered_ids), len(rendered_ids[0])

        pprint(self.core.grid, width=200)
        # pprint(rendered_ids, width=200)

        if type(self.renderer).__name__.lower() != "deterministicrenderer":
            pprint(self.renderer)
            rendered = [[-1 for _ in range(m)] for _ in range(n)]
            for i in range(n):
                for j in range(m):
                    rendered[i][j] = self.core.patterns[rendered_ids[i][j]]

                    red = self.i2c[rendered[i][j].color][0]
                    green = self.i2c[rendered[i][j].color][1]
                    blue = self.i2c[rendered[i][j].color][2]
                    rendered[i][j] = (red, green, blue)

            # pprint(rendered, width=200)
            self.save(rendered, os.path.join(
                'results', name, f"{name}_ml.png"))
