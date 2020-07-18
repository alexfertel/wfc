import numpy as np
from pprint import pformat


class Pattern:
    def __init__(self, matrix: np.array, index=-1, count=1, sample=-1, pos=None):
        self.matrix: np.array = matrix
        self.index = index
        self.count = count
        self.sample = sample
        self.pos = pos

    def __hash__(self):
        return self.index

    def __eq__(self, other):
        return np.equal(self.matrix, other.matrix).all()

    def __str__(self):
        result = f'\n\tIndex: {self.index}\n\t'
        result += f'Weight: {self.count}\n\t'
        result += f'Sample: {self.sample}\n'
        result += pformat(self.matrix, indent=2, width=200)
        return result

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Pattern(np.copy(self.matrix), self.index, self.count)

    @property
    def color(self):
        return self.matrix[0][0]
