import numpy as np

from .wfc import WFCProblem
from .utils import matrices as mxs

class TextureGeneration(WFCProblem):
    def __init__(self, example):
        self.example = np.array(example)
        
        self.p2i = {}
        self.pcount = 0
        self.propagator = {}

    def extract_patterns(self, size):
        """
        This function extracts patterns of size (n x n) from the example image.

        :param size: length of one side of the patterns (They are assumed to be squares) 
        """
        if size < 1:
            return []

        return mxs.overlapping_submatrices(self.example, size)

    def classify_patterns(self, patterns):
        for pat in patterns:
            self.classify_pattern(pat)

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

    def get_id(self, pattern):
        """
        This function returns the mapped identifier of the input pattern.

        :param pattern: The pattern to be mapped.
        """
        string_repr = np.array2string(pattern)
        return self.p2i[string_repr]

    def learn_adjacencies(self, patterns):
        """
        This is what mxm called `Build propagator` in the original algorithm implementation.

        Takes the list of patterns and builds an index data-structure that
        maps an identifier and a direction into a list of identifiers that
        may be adjacent to it.

        :param patterns: The patterns to build the data-structure of.
        """
        # Pre-compute frontier matrix
        frontiers = {}
        for pat in patterns:
            for d in mxs.directions():
                print(pat)
                frontiers[(self.get_id(pat), d)] = mxs.matrix_frontier(pat, d)

        # Build propagator
        propagator = {}
        for lap in patterns:
            lap_id = self.get_id(lap)

            matches = []
            for d in mxs.directions():
                for over in patterns:
                    over_id = self.get_id(over)

                    print(frontiers[(lap_id, d)], frontiers[(over_id, (-d[0], -d[1]))])
                    if frontiers[(lap_id, d)] == frontiers[(over_id, (-d[0], -d[1]))]:
                        matches.append(over_id)
            
            propagator[(lap_id, d)] = matches

        # This takes care of overwriting the old propagator
        self.propagator = propagator
        return self.propagator

    def valid_adjacency(self, id1, id2, **kwargs):
        return id2 in self.propagator[(id1, kwargs['direction'])]

    def render_pattern(self, identifier):
        for p, i in self.p2i.items():
            if identifier == i:
                return p
        return False

    # def generate_4d(self, slots):


