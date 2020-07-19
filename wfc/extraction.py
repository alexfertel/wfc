from functools import reduce, lru_cache
import numpy as np

from wfc.lookup_table import LookupTable
from wfc.pattern import Pattern

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def overlaps(matrix, direction):
    if direction == (-1, 0):  # North
        return matrix[: -1, :]
    if direction == (0, 1):  # East
        return matrix[:, 1:]
    if direction == (1, 0):  # South
        return matrix[1:, :]
    if direction == (0, -1):  # West
        return matrix[:, :-1]

    return False


def compatible(p1, p2, d):
    x, y = d
    m1 = overlaps(p1.matrix, (x, y))
    m2 = overlaps(p2.matrix, (-x, -y))
    return (m1 == m2).all()


def extract_wrapped_pattern(matrix, i, j, size):
    n, m = matrix.shape
    rows = [x % n for x in range(i, i + size)]
    cols = [y % m for y in range(j, j + size)]
    return matrix[rows][:, cols]


def extract_submatrices(pattern_extractor, size, matrix):
    n, m = matrix.shape

    submatrices = []
    for i in range(n):
        for j in range(m):
            sm = pattern_extractor(matrix, i, j, size)
            submatrices.append(Pattern(sm, pos=(i, j)))

    return submatrices


def extract_patterns(samples, extractor):
    extracted = []
    for index, sample in enumerate(samples):
        submatrices = extractor(sample)
        for submatrix in submatrices:
            submatrix.sample = index

        extracted.append(submatrices)

    return extracted


def transform(allow_rotations, allow_reflections, pattern):
    patterns = [pattern]
    if allow_rotations or allow_reflections:
        sm = None
        for _ in range(3):
            if allow_rotations:
                sm = np.rot90(pattern)
                patterns.append(sm)

            if allow_reflections:
                sm = np.flip(sm)
                patterns.append(sm)

    return patterns


def transform_patterns(patterns, transformer):
    return reduce(lambda x, y: x + transformer(y), patterns, [])


def fill_table(patterns, table, can_overlap):
    for p1 in patterns:
        for p2 in patterns:
            for x, y in dirs:
                d = (x, y)
                if can_overlap(p1, p2, d):
                    table[d][p1.index].add(p2.index)
                    table[(-x, -y)][p2.index].add(p1.index)

    return table


def distance(p1, p2, sample):
    n, m = sample.shape
    x1, y1 = p1.pos
    x2, y2 = p2.pos

    dx = abs(x1 - x2)
    if dx > n / 2:
        dx = n - dx

    dy = abs(y1 - y2)
    if dy > m / 2:
        dy = m - dy

    return dx + dy


def measure(ppatterns, samples, delta):
    n = len(ppatterns)

    for index, pp in enumerate(ppatterns):
        pp.index = index

    deltas = []
    for sample in samples:
        height, width = sample.shape
        diameter = (height + width) / 2
        deltas.append(1 + delta * (diameter - 1))

    distance_table = [[(float('inf'), 0) for _ in range(n)] for _ in range(n)]

    def overlap_somehow(p1, p2):
        overlapped = False
        for d in dirs:
            overlapped = overlapped or compatible(p1, p2, d)

        return overlapped

    for i in range(n):
        for j in range(n):
            pi = ppatterns[i]
            pj = ppatterns[j]
            if pi.sample == pj.sample and overlap_somehow(pi, pj):
                dist = distance(pi, pj, samples[pi.sample])
                distance_table[i][j] = dist, deltas[pi.sample]
                distance_table[j][i] = dist, deltas[pi.sample]

    return distance_table
