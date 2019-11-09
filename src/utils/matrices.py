import numpy as np

def overlapping_submatrices(matrix, size):
    n, m = matrix.shape
    submatrices = []
    for i in range(n - size + 1):
        for j in range(m - size + 1):
            submatrices.append(matrix[i: i + size, j: j + size])

    return submatrices


def matrix_edges(matrix, side):
    if not 0 <= side < 5:
        raise Exception(f"`side` should be one of [0, 1, 2, 3].")

    n, m = matrix.shape
    if side == 0:
        return matrix[0, 0: n]
    if side == 1:
        return matrix[0: n, m - 1]
    if side == 2:
        return matrix[n - 1, 0: m]
    if side == 3:
        return matrix[0: n, 0]


