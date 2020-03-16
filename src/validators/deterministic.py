
from collections import defaultdict

from .validator import Validator
from ..utils import compatible, dirs
from ..lookup_table import LookupTable
from pprint import pprint


class DeterministicValidator(Validator):
    def __init__(self):
        super().__init__()

        self.lt = LookupTable()

    def learn(self, patterns):
        # Learn adjacencies
        for p1 in patterns:
            for p2 in patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1.matrix, p2.matrix, d):
                        self.lt[d][p1.index].add(p2.index)
                        self.lt[(-x, -y)][p2.index].add(p1.index)
        pprint(str(self.lt))
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

        # # Prune adjacencies
        # for x, y in dirs:
        #     d = (x, y)
        #     for pattern in patterns:
        #         self.lt[d][p.index] -= local_table


        return self

    def valid(self, identifier, direction):
        return self.lt[direction][identifier]
