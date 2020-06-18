import numpy as np

from .deterministic import DeterministicValidator
from ..utils import compatible, dirs, d2i, in_range
from ..lookup_table import LookupTable
from pprint import pprint
from collections import defaultdict


class Generalizer(DeterministicValidator):
    def __init__(self, alpha=.0):
        super().__init__()

    def learn(self, patterns):
        pprint(patterns.shape, indent=2, width=100)
        n, m = patterns.shape
        for i in range(n):
            for j in range(m):
                for dx, dy in dirs:
                    d = (dx, dy)
                    x, y = i + dx, j + dy
                    p1 = patterns[i][j]
                    p2 = patterns[x][y]
                    if in_range((x, y), patterns) and compatible(p1.matrix, p2.matrix, d):
                        self.lt[d][p1.index].add(p2.index)
                        self.lt[(-dx, -dy)][p2.index].add(p1.index)

        return self
