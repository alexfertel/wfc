import numpy as np

from sklearn.cluster import KMeans
from .deterministic import DeterministicValidator
from ..utils import compatible, dirs, d2i
from ..lookup_table import LookupTable
from pprint import pprint
from collections import defaultdict

class KMeansValidator(DeterministicValidator):
    def __init__(self):
        super().__init__()

        self.clustering = None


    def postprocess(self, patterns):
        n = len(patterns)
        self.clustering = KMeans(n_clusters=6)
        # pprint(patterns)
        pprint(self.lt, indent=2, width=100)

        self.matrix = self.lt.get_matrix(n)
        self.clustering.fit(self.matrix)

        # pprint(self.clustering.cluster_centers_indices_)
        pprint("Clustering Labels:")
        pprint(self.clustering.labels_)

        # Make clusters
        clusters = defaultdict(set)
        for i in range(len(self.clustering.labels_)):
            for j in range(len(self.clustering.labels_)):
                if self.clustering.labels_[i] == self.clustering.labels_[j]:
                    clusters[i].add(j)

        pprint("Clusters:")
        pprint(clusters)

        for direction in dirs:
            d = d2i(direction)
            
            for p in range(n):
                # New set
                result = set()
                for pattern in self.lt[direction][p]:
                    result |= clusters[pattern]

                self.lt[direction][p] = result

        pprint("Look-up Table:")
        pprint(self.lt)

        return self
