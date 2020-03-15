import numpy as np

class Pattern:
    def __init__(self, matrix, index=-1):
        self.matrix = matrix
        self.index = index
    
    def __eq__(self, other):
        return np.equal(self.matrix, other.matrix)

    @property
    def color(self):
        return self.matrix[0][0]

    
