import numpy as np
from pprint import pformat


class Pattern:
    def __init__(self, matrix: np.array, index=-1, count=1):
        self.matrix: np.array = matrix
        self.index = index
        self.count = count

    def __hash__(self):
        return self.index

    def __eq__(self, other):
        return np.equal(self.matrix, other.matrix).all()

    def __str__(self):
        result = f'Index: {self.index}\n '
        result += f'Weight: {self.count}\n '
        result += pformat(self.matrix, indent=2, width=200)
        return result

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Pattern(np.copy(self.matrix), self.index, self.count)

    @property
    def color(self):
        return self.matrix[0][0]
