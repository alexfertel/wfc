from sklearn.cluster import AffinityPropagation
import numpy as np

from .validator import Validator
from ..utils import compatible, dirs, d2i
from ..lookup_table import LookupTable
# from ..cluster_map import ClusterMap
from pprint import pprint


class AffinityValidator(Validator):
    def __init__(self):
        super().__init__()

        self.lt = LookupTable()

        self.clustering = AffinityPropagation()

    def learn(self, patterns):
        # Learn adjacencies
        for p1 in patterns:
            for p2 in patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1.matrix, p2.matrix, d):
                        self.lt[d][p1.index].add(p2.index)
                        self.lt[(-x, -y)][p2.index].add(p1.index)
        # pprint(str(self.lt))
        return self

    def prune(self, patterns):
        # Learn adjacencies
        local_table = LookupTable()
        for p1 in patterns:
            for p2 in patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1.matrix, p2.matrix, d):
                        local_table[d][p1.index].add(p2.index)
                        local_table[(-x, -y)][p2.index].add(p1.index)

        # Prune adjacencies
        for x, y in dirs:
            d = (x, y)
            for p in patterns:
                self.lt[d][p.index] -= local_table[d][p.index]

        return self

    def valid(self, identifier, direction):
        label = self.clustering.labels_[identifier]
        n = len(self.matrix[0]) // 4

        vector = self.lt.get_matrix(n)[label]

        # pprint(vector, width=500)

        d = d2i(direction)

        dir_window = vector[d * n: (d + 1) * n]

        result = set()
        for index, bit in enumerate(dir_window): 
            if bit: result.add(index)

        return result
        # return self.lt[direction][identifier]

    def postprocess(self, patterns):
        self.matrix = self.lt.get_matrix(len(patterns))
        self.clustering.fit(self.matrix)

        return self

