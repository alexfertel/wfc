import numpy as np

def overlapping_submatrices(matrix, size):
    n, m = matrix.shape
    submatrices = []
    for i in range(n - size + 1):
        for j in range(m - size + 1):
            submatrices.append(matrix[i: i + size, j: j + size])

    return submatrices


def matrix_frontier(matrix, direction):
    dx, dy = direction
    d = [-1, 0, 1]

    if not dx in d or not dy in d:
        raise Exception(f"`dx` and `dy` must be one of [-1, 0, 1].")

    n, m = matrix.shape
    
    if direction == (0, -1):  # North
        return matrix[0, 0: m]
    if direction == (1, -1):  # Northeast
        return matrix[0, m - 1]
    if direction == (1, 0):  # East
        return matrix[0: n, m - 1]
    if direction == (1, 1):  # Southeast
        return matrix[n - 1, m - 1]
    if direction == (0, 1):  # South
        return matrix[n - 1, 0: m]
    if direction == (-1, 1):  # Southwest
        return matrix[n - 1, 0]
    if direction == (-1, 0):  # West
        return matrix[0: n, 0]
    if direction == (-1, -1):  # Northwest
        return matrix[0, 0]

    return False


