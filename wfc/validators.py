import numpy as np

from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from scipy.spatial.distance import pdist

from wfc.lookup_table import LookupTable
from wfc.extraction import dirs, compatible, fill_table


def validator(alpha, distance_table):
    lookup_table = LookupTable()

    def g(p1, p2):
        dist = float('inf')
        delta = 0
        for id1 in p1.family:
            for id2 in p2.family:
                d, delta = distance_table[id1][id2]
                dist = min(dist, d)

        return 1 if dist <= delta else 0

    def f(p1, p2, d):
        return 1 if compatible(p1, p2, d) else 0

    def can_overlap(p1, p2, d):
        return f(p1, p2, d) * g(p1, p2)

    def learn(patterns):
        fill_table(patterns, lookup_table, can_overlap)
        return lookup_table

    def prune(patterns):
        local_table = fill_table(patterns, LookupTable(), can_overlap)

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
            distance_matrix = pdist(matrix, metric='sqeuclidean')
            max_dist = np.max(distance_matrix)
            min_dist = np.min(distance_matrix)
            param = -(min_dist + (max_dist - min_dist) * (1 - alpha)) + 1
            return AffinityPropagation(preference=param)

        clustering = init_affinity()
    
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

    def valid(direction, identifier):
        return lookup_table[direction][identifier]

    def process(positive, negative):
        learn(positive)
        prune(negative)
        postprocess(positive)

    return process, valid, lookup_table
