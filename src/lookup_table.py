from collections import defaultdict
from .utils import d2i

class LookupTable:
    def __init__(self):
        self.tables = [defaultdict(set) for i in range(4)]
        
    def __getitem__(self, key):
        return self.tables[d2i(key)]
        
    def __setitem__(self, key, value):
        self.tables[d2i(key)] = value
