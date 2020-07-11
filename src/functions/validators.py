from src.lookup_table import LookupTable
from src.utils import dirs, compatible


def deterministic(*args, **kwargs):
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

    def valid(direction, identifier):
        return lookup_table[direction][identifier]

    def process(positive, negative):
        learn(positive)
        prune(negative)

    return process, valid
