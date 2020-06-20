import numpy as np

from .deterministic import DeterministicValidator
from ..utils import compatible, dirs, d2i, in_range
from ..lookup_table import LookupTable
from pprint import pprint
from collections import defaultdict


class Generalizer(DeterministicValidator):
    def __init__(self, alpha=.0):
        super().__init__()

    def learn(self, patterns, shape):
        n, m = shape
        for index in range(n * m):
            i = index // n
            j = index % m
            p1 = patterns[i * n + j]
            for dx, dy in dirs:
                d = (dx, dy)
                x, y = i + dx, j + dy
                print(x * n + y)
                if 0 <= x * n + y < n * m:
                    p2 = patterns[x * n + y]
                    if compatible(p1.matrix, p2.matrix, d):
                        self.lt[d][p1.index].add(p2.index)
                        self.lt[(-dx, -dy)][p2.index].add(p1.index)

        return self
