import numpy as np

from .wfc import WFCProblem
from .utils import matrices

class TextureGeneration(WFCProblem):
    def __init__(self, example):
        self.example = np.array(example)
        
        self.p2i = {}
        self.pcount = 0

    def extract_patterns(self, size):
        """
        This function extracts patterns of size (n x n) from the example image.

        :param size: length of one side of the patterns (They are assumed to be squares) 
        """
        if size < 1:
            return []

        return matrices.overlapping_submatrices(self.example, size)


    def classify_pattern(self, pattern):
        """
        This function is inherited from WFCProblem.

        For now we just map an integer to each pattern.
        """
        string_repr = np.array2string(pattern)
        if string_repr in self.p2i:
            return self.p2i[string_repr]

        self.p2i[string_repr] = self.pcount
        self.pcount += 1
        return self.pcount - 1

    def render_pattern(self, identifier):
        for p, i in self.p2i.items():
            if identifier == i:
                return p
        return False
