import numpy as np

from sklearn.cluster import AffinityPropagation
from .deterministic import DeterministicValidator
from ..utils import compatible, dirs, d2i
from ..lookup_table import LookupTable
from pprint import pprint
from collections import defaultdict
from scipy.spatial.distance import pdist

class AffinityValidator(DeterministicValidator):
    def __init__(self, alpha=.0):
        super().__init__()

        self.alpha = alpha
        self.clustering = None

    def postprocess(self, patterns):
        n = len(patterns)
        self.matrix = self.lt.get_matrix(n)

        m = np.max(pdist(self.matrix))
        param = m * self.alpha

        pprint(param)

        self.clustering = AffinityPropagation(preference=param)

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
