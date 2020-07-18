from collections import defaultdict
from pprint import pformat, pprint


def d2i(direction):
    x, y = direction

    if x == -1:
        return 0
    if y == 1:
        return 1
    if x == 1:
        return 2
    if y == -1:
        return 3

    raise Exception(f'`direction` arg {direction} is not a valid direction.')


class LookupTable:
    def __init__(self):
        self.tables = [defaultdict(set) for _ in range(4)]

    def __getitem__(self, key):
        return self.tables[d2i(key)]

    def __setitem__(self, key, value):
        self.tables[d2i(key)] = value

    def __str__(self):
        result = f'North: \n{pformat(self.tables[0], width=100, indent=2)}\n'
        result += f'East: \n{pformat(self.tables[1], width=100, indent=2)}\n'
        result += f'South:\n{pformat(self.tables[2], width=100, indent=2)}\n'
        result += f'West: \n{pformat(self.tables[3], width=100, indent=2)}\n'
        return result

    def __repr__(self):
        return self.__str__()

    def get_matrix(self, pcount):
        table = [[0 for _ in range(4 * pcount)] for _ in range(pcount)]
        for p1 in range(pcount):
            for d in range(4):
                for p2 in range(pcount):
                    if p2 in self.tables[d][p1]:
                        table[p1][p2 + d * pcount] = 1

        return table
