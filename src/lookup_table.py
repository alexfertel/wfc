from collections import defaultdict
from .utils import d2i
from pprint import pformat, pprint

class LookupTable:
    def __init__(self):
        self.tables = [defaultdict(set) for i in range(4)]

    def __getitem__(self, key):
        return self.tables[d2i(key)]

    def __setitem__(self, key, value):
        self.tables[d2i(key)] = value

    def __str__(self):
        result =  f'North:\n{pformat(self.tables[0], width=200, indent=2)}\n'
        result += f'East: \n{pformat(self.tables[1], width=200, indent=2)}\n'
        result += f'South:\n{pformat(self.tables[2], width=200, indent=2)}\n'
        result += f'West: \n{pformat(self.tables[3], width=200, indent=2)}\n'
        return result

    def __repr__(self):
        return self.__str__()

    def get_matrices(self, pcount):
        matrices = []
        for ddict in self.tables:
            table = [[0 for _ in range(pcount)] for _ in range(pcount)]
            for p1 in range(pcount):
                for p2 in range(pcount):
                    if p2 in ddict[p1]:
                        table[p1][p2] = 1

            matrices.append(table)
        
        return matrices
