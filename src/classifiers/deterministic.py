import numpy as np

from .classifier import Classifier
from ..pattern import Pattern


class DeterministicClassifier(Classifier):
    def __init__(self):
        super().__init__()
        
    def classify_patterns(self, patterns):
        unique, counts = np.lib.arraysetops.unique(patterns, return_counts=True, axis=0)
        patterns = [Pattern(pat, index) for index, pat in enumerate(unique)]
        return patterns, counts

    def classify_pattern(self, pattern):
        pass