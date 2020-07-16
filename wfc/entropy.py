import numpy as np

from random import random


class Entropy:
    def __init__(self, weights, patterns):
        self.sow = sum(weights)
        self.sowl = sum(map(lambda p: weights[p.index] * np.log(weights[p.index]), patterns))
        self.noise = random.random() / 1e5

    @property
    def entropy(self):
        return np.log(self.sow) - self.sowl / self.sow + self.noise

    def __lt__(self, other):
        return self.entropy < other.entropy

    def __str__(self):
        return str(self.entropy)

    def __repr__(self):
        return self.__str__()


