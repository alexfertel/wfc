from PIL import Image
import os
import numpy as np
from pprint import pprint

class Texture:
    def __init__(self, name):
        self.bitmap = Image.open("images/{0}.png".format(name))
        self.SMX = self.bitmap.size[0]
        self.SMY = self.bitmap.size[1]
        
        # .sample is an array of arrays that holds the index values for colors 
        # as found in the source image
        self.sample = [[0 for _ in range(self.SMY)] for _ in range(self.SMX)]
        # .colors is the list of colors that are found in the source image
        self.colors = []
        
        # This initializes the .sample array with the color index values.
        # It loops over the pixels in the source bitmap, adds the color to the
        # list of colors if it is new, and sets the .sample x,y value to the
        # index of the color in the list of colors.
        for y in range(0, self.SMY):
            for x in range(0, self.SMX):
                a_color = self.bitmap.getpixel((x, y))
                color_exists = [c for c in self.colors if c == a_color]
                if len(color_exists) < 1:
                    self.colors.append(a_color)
                samp_result = [i for i,v in enumerate(self.colors) if v == a_color]
                self.sample[x][y] = samp_result[0]
                
        
        self.color_count = len(self.colors)

        # pprint(self.sample)
        # pprint(self.colors)


    def save(self, grid, name):
        rgb = self.compute_wave_colors(grid)

        data = np.int8(rgb)
        image = Image.fromarray(data, mode="RGB")

        image.save(f"results/{name}.bmp", compression=0)

    def compute_wave_colors(self, grid):
        n, m = len(grid), len(grid[0])

        rgb = [[None for _ in range(n)] for _ in range(m)]

        for i in range(n):
            for j in range(m):
                red, green, blue = (0, 0, 0)
                contributors = [p for p in grid[i][j].patterns if grid[i][j].possibilities[p.index]]

                for allowed_pattern in contributors:
                    red += self.colors[allowed_pattern.color][0]
                    green += self.colors[allowed_pattern.color][1]
                    blue += self.colors[allowed_pattern.color][2]

                N = len(contributors)
                rgb[i][j] = (red / N, green / N, blue / N)
        
        return rgb
