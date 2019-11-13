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


def matrix_frontier(matrix, direction):
    if not direction in directions():
        raise Exception(f"`direction` must be one of `directions()`.")

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

def overlaps(lap, over):


    olaps = [(matrix_frontier(lap, d1), matrix_frontier(over, d2)) for d1 in directions() for d2 in directions()]
    return filter(lambda x: x[0] == x[1], olaps)



        
    
