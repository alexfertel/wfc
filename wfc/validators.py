import numpy as np

from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from scipy.spatial.distance import pdist

from wfc.lookup_table import LookupTable
from wfc.utils import dirs, compatible, d2i


def validator(alpha):
    lookup_table = LookupTable()

    def fill_table(patterns, table):
        for p1 in patterns:
            for p2 in patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1.matrix, p2.matrix, d):
                        table[d][p1.index].add(p2.index)
                        table[(-x, -y)][p2.index].add(p1.index)

        return table

    def learn(patterns):
        fill_table(patterns, lookup_table)
        return lookup_table

    def prune(patterns):
        local_table = fill_table(patterns, LookupTable())

        # Prune the adjacency
        for x, y in dirs:
            d = (x, y)
            for p in patterns:
                lookup_table[d][p.index] -= local_table[d][p.index]

        return lookup_table

    def postprocess(patterns):
        n = len(patterns)
        matrix = lookup_table.get_matrix(n)

        def init_kmeans():
            """
            alpha for KMeans
            1 + (max - min) * alpha
            """
            param = int(1 + (n - 1) * alpha)
            return KMeans(n_clusters=param)

        def init_affinity():
            m = np.max(pdist(matrix))
            param = m * alpha
            return AffinityPropagation(preference=param)

        clustering = init_kmeans()

        clustering.fit(matrix)

        clusters = defaultdict(set)
        for i in range(len(clustering.labels_)):
            for j in range(len(clustering.labels_)):
                if clustering.labels_[i] == clustering.labels_[j]:
                    clusters[i].add(j)

        for direction in dirs:
            for p in range(n):
                result = set()
                for pattern in lookup_table[direction][p]:
                    result |= clusters[pattern]

                lookup_table[direction][p] = result

    def valid(direction, base_id, neighbor_id):
        return neighbor_id in lookup_table[direction][base_id]

    def process(positive, negative):
        learn(positive)
        prune(negative)
        # TODO: Why are we using `ppaterns` here?
        postprocess(positive)

    return process, valid
