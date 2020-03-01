# 4-neighbourhood
import numpy as np

from pprint import pprint

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
# dirs = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x != 0 or y != 0]


def directions():
    return [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x != 0 or y != 0]


def overlapping_submatrices(matrix, size):
    n, m = matrix.shape
    submatrices = []
    for i in range(n - size + 1):
        for j in range(m - size + 1):
            submatrices.append(matrix[i: i + size, j: j + size])

    return submatrices


def matrix_direction(matrix, direction):
    n, m = matrix.shape

    if direction == (0, -1):  # North
        return matrix[: -1, :]
    if direction == (1, 0):  # East
        return matrix[:, 1:]
    if direction == (0, 1):  # South
        return matrix[1:, :]
    if direction == (-1, 0):  # West
        return matrix[:, :-1]

    return False


def overlaps(lap, over):
    olaps = [(matrix_frontier(lap, d1), matrix_frontier(over, d2))
             for d1 in directions() for d2 in directions()]
    return filter(lambda x: x[0] == x[1], olaps)


def render(grid):
    y, x = len(grid[0]), len(grid)
    result = [[-1 for _ in range(y)] for _ in range(x)]
    for i in range(x):
        for j in range(y):
            result[i][j] = grid[i][j].color
    return result


def compatible(p1, p2, d):
    x, y = d
    m1 = matrix_lap(p1.matrix, (x, y))
    m2 = matrix_lap(p2.matrix, (-x, -y))
    return (m1 == m2).all()


def matrix_lap(matrix, direction):
    n, m = matrix.shape

    if direction == (0, -1):  # North
        return matrix[: -1, :]
    if direction == (1, 0):  # East
        return matrix[:, 1:]
    if direction == (0, 1):  # South
        return matrix[1:, :]
    if direction == (-1, 0):  # West
        return matrix[:, :-1]

    return False


def in_range(pos, grid):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def extract_submatrices(matrix, size, pattern_extractor):
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

def find(elements, value):
    value = value.lower()
    for obj in elements:
        if obj.__name__.lower() == value:
            return obj
    raise ValueError(f"{value} not found in {[e.__name__ for e in elements]}")

if __name__ == "__main__":
    arr = np.arange(16).reshape((4, 4))
    pprint(extract_submatrices(arr, 3, extract_wrapped_pattern))
