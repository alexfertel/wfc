from collections import defaultdict
from .utils import d2i
from pprint import pformat

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
