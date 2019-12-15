# 4-neighbourhood
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]


import numpy as np

def directions():
    return [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)]

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
    olaps = [(matrix_frontier(lap, d1), matrix_frontier(over, d2)) for d1 in directions() for d2 in directions()]
    return filter(lambda x: x[0] == x[1], olaps)


def render(grid):
    y, x = len(grid[0]), len(grid)
    result = [[-1 for _ in range(y)] for _ in range(x)]
    for i in range(x):
        for j in range(y):
            result[i][j] = grid[i][j].color
    return result
