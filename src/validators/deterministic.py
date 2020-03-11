
from collections import defaultdict

from .validator import Validator
from ..utils import compatible, dirs
from ..lookup_table import LookupTable
from pprint import pprint

class DeterministicValidator(Validator):
    def __init__(self, patterns):
        super().__init__()

        self.patterns = patterns
        self.adjacency_rules = defaultdict(set)

        self.learn_adjacencies()

    def learn_adjacencies(self):
        # Learn adjacencies
        for p1 in self.patterns:
            for p2 in self.patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1.matrix, p2.matrix, d):
                        self.adjacency_rules[(p1.index, d)].add(p2.index)
                        self.adjacency_rules[(p2.index, (-x, -y))].add(p1.index)
        pprint(self.adjacency_rules)
        return self

    def valid_adjacencies(self, identifier, direction):
        return self.adjacency_rules[identifier, direction]