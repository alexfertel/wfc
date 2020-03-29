import numpy as np

from .classifier import Classifier
from ..pattern import Pattern

from pprint import pprint


class DeterministicClassifier(Classifier):
    def __init__(self):
        super().__init__()

        self.patterns = []

    def classify_patterns(self, patterns):
        unique, counts = np.lib.arraysetops.unique(
            patterns, return_counts=True, axis=0)

        for index, pat in enumerate(unique):
            pattern = Pattern(pat, index, counts[index])
            self.update_set(pattern)

        # Making it backwards compatible
        counts = [p.count for p in self.patterns]
        return self.patterns, counts

    def classify_pattern(self, pattern):
        if pattern in self.patterns:
            return self.patterns[self.patterns.index(pattern)]

        pat = Pattern(pattern)
        self.update_set(pat)
        return pat

    def update_set(self, pattern):
        if pattern in self.patterns:
            for pat in self.patterns:
                if pat == pattern:
                    pat.count += pattern.count
                    pattern.index = pat.index
        else:
            pattern.index = len(self.patterns)        
            self.patterns.append(pattern)
