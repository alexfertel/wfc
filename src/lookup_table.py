from collections import defaultdict
from .utils import d2i


class LookupTable:
    def __init__(self):
        self.tables = [defaultdict(set) for i in range(4)]

    def __getitem__(self, key):
        return self.tables[d2i(key)]

    def __setitem__(self, key, value):
        self.tables[d2i(key)] = value

    def __str__(self):
        result =  f'North:\n{self.tables[0]}\n'
        result += f'East: \n{self.tables[1]}\n'
        result += f'South:\n{self.tables[2]}\n'
        result += f'West: \n{self.tables[3]}\n'
        return result
