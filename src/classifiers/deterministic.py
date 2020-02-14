import numpy as np

from .classifier import Classifier
from ..pattern import Pattern

from pprint import pprint

class DeterministicClassifier(Classifier):
    def __init__(self):
        super().__init__()

    def classify_patterns(self, patterns):
        unique, counts = np.lib.arraysetops.unique(
            patterns, return_counts=True, axis=0)
        patterns = [Pattern(pat, index) for index, pat in enumerate(unique)]
        return patterns, counts

    def classify_pattern(self, pattern):
        pass

    def extract_pattern(self, example, i, j, k):
        n, m = example.shape
        rows = [i % n for i in range(i, i + k)]
        cols = [j % m for j in range(j, j + k)]
        return example[rows][:, cols]
        # return example[i: i + k, j: j + k]

