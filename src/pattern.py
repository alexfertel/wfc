import numpy as np

class Pattern:
    def __init__(self, matrix, index=-1, count=1):
        self.matrix = matrix
        self.index = index
        self.count = count
    
    def __hash__(self):
        return self.index

    def __eq__(self, other):
        return np.equal(self.matrix, other.matrix).all()

    @property
    def color(self):
        return self.matrix[0][0]

    
