import numpy as np

from .affinity import AffinityValidator
from ..utils import compatible, dirs, d2i
from ..lookup_table import LookupTable
from pprint import pprint


class UnionAffinityValidator(AffinityValidator):
    def __init__(self):
        super().__init__()

    def valid(self, identifier, direction):
        n = len(self.matrix[0]) // 4
        d = d2i(direction)

        result = set()
        for label in self.clustering.labels_:
            if self.clustering.labels_[identifier] == label:
                vector = self.matrix[label]
                dir_window = vector[d * n: (d + 1) * n]

                for index, bit in enumerate(dir_window): 
                    if bit: result.add(index)

        # pprint(result)
        return result
        # return self.lt[direction][identifier]


    def postprocess(self, patterns):
        pprint(patterns)
        n = len(patterns)
        self.matrix = self.lt.get_matrix(n)
        self.clustering.fit(self.matrix)

        pprint(self.clustering.cluster_centers_indices_)
        pprint(self.clustering.labels_)
        pprint(self.clustering.affinity)
        pprint(self.clustering.affinity_matrix_)

        for p in range(n):
            cluster = self.clustering.labels_[p]

            # vector = self.matrix[label]

            # pprint(vector, width=500)
            
            for direction in dirs:
                d = d2i(direction)

                result = set()
                print(f"Pattern {p} - Dir {d} - Cluster {cluster}")
                for label in self.clustering.labels_:
                    if self.clustering.labels_[label] == cluster:
                        vector = self.matrix[label]
                        
                        dir_window = vector[d * n: (d + 1) * n]

                        for index, bit in enumerate(dir_window):
                            if bit: result.add(index)

                self.lt[direction][p] = result

        return self
