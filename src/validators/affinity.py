from sklearn.cluster import AffinityPropagation
import numpy as np

from .deterministic import DeterministicValidator
from ..utils import compatible, dirs, d2i
from ..lookup_table import LookupTable
from pprint import pprint
from collections import defaultdict


class AffinityValidator(DeterministicValidator):
    def __init__(self):
        super().__init__()

        self.clustering = AffinityPropagation()

    def postprocess(self, patterns):
        n = len(patterns)
        self.matrix = self.lt.get_matrix(n)
        self.clustering.fit(self.matrix)

        # Make clusters
        clusters = defaultdict(set)
        for i in range(len(self.clustering.labels_)):
            if self.clustering.labels_[i] == self.clustering.cluster_centers_indices_[0]:
                clusters[i].add(self.clustering.cluster_centers_indices_[0])
            else:
                clusters[i].add(self.clustering.cluster_centers_indices_[1])
            
        pprint(clusters)

        for p in range(len(patterns)):
            label = self.clustering.labels_[p]

            vector = self.matrix[label]

            # pprint(vector, width=500)

            for direction in dirs:
                d = d2i(direction)

                dir_window = vector[d * n: (d + 1) * n]

                result = set()
                for index, bit in enumerate(dir_window):
                    if bit:
                        result |= clusters[index]

                self.lt[direction][p] = result

        return self
