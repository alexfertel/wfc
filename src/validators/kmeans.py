import numpy as np

from sklearn.cluster import KMeans
from .deterministic import DeterministicValidator
from ..utils import compatible, dirs, d2i
from ..lookup_table import LookupTable
from pprint import pprint
from collections import defaultdict


class KMeansValidator(DeterministicValidator):
    def __init__(self, alpha=.0):
        super().__init__()

        self.alpha = alpha
        self.clustering = None

    def postprocess(self, patterns):
        n = len(patterns)
        self.matrix = self.lt.get_matrix(n)

        # alpha for KMeans
        # 1 + (max - min) * alpha
        param = int(1 + (n - 1) * self.alpha)
        self.clustering = KMeans(n_clusters=param)

        self.clustering.fit(self.matrix)

        # Make clusters
        clusters = defaultdict(set)
        for i in range(len(self.clustering.labels_)):
            for j in range(len(self.clustering.labels_)):
                if self.clustering.labels_[i] == self.clustering.labels_[j]:
                    clusters[i].add(j)

        for direction in dirs:
            d = d2i(direction)

            for p in range(n):
                # New set
                result = set()
                for pattern in self.lt[direction][p]:
                    result |= clusters[pattern]

                self.lt[direction][p] = result

        return self
