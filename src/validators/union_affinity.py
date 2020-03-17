import numpy as np

from .affinity import AffinityValidator
from ..utils import compatible, dirs, d2i
from ..lookup_table import LookupTable
from pprint import pprint
from collections import defaultdict

class UnionAffinityValidator(AffinityValidator):
    def __init__(self):
        super().__init__()

    def postprocess(self, patterns):
        pprint(patterns)
        n = len(patterns)
        self.matrix = self.lt.get_matrix(n)
        self.clustering.fit(self.matrix)

        pprint(self.clustering.cluster_centers_indices_)
        pprint(self.clustering.labels_)

        # Make clusters
        clusters = defaultdict(set)
        for i in range(len(self.clustering.labels_)):
            for j in range(len(self.clustering.labels_)):
                if self.clustering.labels_[i] == self.clustering.labels_[j] and i != j:
                    clusters[i].add(j)

        for p in range(n):
            label = self.clustering.labels_[p]
            vector = self.matrix[label]

            for direction in dirs:
                d = d2i(direction)

                dir_window = vector[d * n: (d + 1) * n]

                result = set()
                for index, bit in enumerate(dir_window):
                    if bit:
                        result |= clusters[index]

                self.lt[direction][p] = result

        return self
