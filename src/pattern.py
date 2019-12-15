class Pattern:
    def __init__(self, matrix, index=-1):
        self.matrix = matrix
        self.index = index
    
    @property
    def color(self):
        return self.matrix[0][0]

    
