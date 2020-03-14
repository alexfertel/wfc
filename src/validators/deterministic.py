
from collections import defaultdict

from .validator import Validator
from ..utils import compatible, dirs
from ..lookup_table import LookupTable
from pprint import pprint

class DeterministicValidator(Validator):
    def __init__(self, patterns):
        super().__init__()

        self.patterns = patterns
        self.lt = LookupTable()
        
        self.learn_adjacencies()

    def learn_adjacencies(self):
        # Learn adjacencies
        for p1 in self.patterns:
            for p2 in self.patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1.matrix, p2.matrix, d):
                        self.lt[d][p1.index].add(p2.index)
                        self.lt[(-x, -y)][p2.index].add(p1.index)
        pprint(str(self.lt))
        return self

    def valid_adjacencies(self, identifier, direction):
        return self.lt[direction][identifier]