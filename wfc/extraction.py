from functools import reduce

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def matrix_lap(matrix, direction):
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
    m1 = matrix_lap(p1, (x, y))
    m2 = matrix_lap(p2, (-x, -y))
    return (m1 == m2).all()


def extract_submatrices(pattern_extractor, size, matrix):
    n, m = matrix.shape
    N = size

    submatrices = []
    for i in range(n):
        for j in range(m):
            sm = pattern_extractor(matrix, i, j, N)
            submatrices.append(sm)

    return submatrices


def extract_wrapped_pattern(matrix, X, Y, size):
    n, m = matrix.shape
    rows = [x % n for x in range(X, X + size)]
    cols = [y % m for y in range(Y, Y + size)]
    return matrix[rows][:, cols]


def extract_patterns(samples, extractor):
    return reduce(lambda x, y: x + extractor(y), samples, [])


def transform_patterns(patterns, transformer):
    return reduce(lambda x, y: x + transformer(y), patterns, [])


def measure(patterns):
    def unravel_index(index):
        n = len(patterns)

        return index / n

        for index, pattern in enumerate(patterns):
