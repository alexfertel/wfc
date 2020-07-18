from functools import reduce
import numpy as np

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
    m1 = overlaps(p1, (x, y))
    m2 = overlaps(p2, (-x, -y))
    return (m1 == m2).all()


def extract_submatrices(pattern_extractor, size, matrix):
    n, m = matrix.shape

    submatrices = []
    for i in range(n):
        for j in range(m):
            sm = pattern_extractor(matrix, i, j, size)
            submatrices.append(sm)

    return submatrices


def extract_wrapped_pattern(matrix, i, j, size):
    n, m = matrix.shape
    rows = [x % n for x in range(i, i + size)]
    cols = [y % m for y in range(j, j + size)]
    return matrix[rows][:, cols]


def extract_patterns(samples, extractor):
    return [extractor(sample) for sample in samples]


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


def measure(patterns):
    print(patterns)

    def unravel_index(index):
        n = len(patterns)

        return index / n

        # for index, pattern in enumerate(patterns):
