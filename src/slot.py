import numpy as np

class Slot:
    def __init__(self, pos):
        self.pos = pos

        # This is used when rendering the slot.
        self.color = -1

        # This is the possibility space of the slot.
        self.possibilities = []
        self.patterns = []

        # We maintain a cummulative frequency array, where we store
        # the relative frequencies, so when sampling the probability
        # distribution of the possibilities, choosing the slot
        # corresponding to a value is easier.
        self.cummulativeFrequencies = []

        # These properties aid when calculating entropy;
        # they are used to make entropy computation constant.
        self.sumOfWeights = 0
        self.sumOfWeightsLogs = 0

        # Applying noise to the entropy, so we don't have to break ties.
        # Initialize a tiny random value.
        self.noise = np.random.ranf() / 1e5

        # Wether the cell is collapsed or not. A heap of the slots is
        # kept in order to quickly retrieve the slot with the minimum
        # entropy, each time a slot's entropy varies, we push it into 
        # the heap, resulting in the possibility of having the same
        # slot in the heap, thus needing to know if a cell is collapsed
        # when popping it from the heap.
        self.collapsed = False



    # Make the set of slots a lattice.
    def __lt__(self, other):
        return self.entropy < other.entropy
    
    # A slot is represented by its color
    def __str__(self):
        return str(self.color)

    def __repr__(self):
        return self.__str__()


    @property
    def entropy(self):
        """
        This is the uncertainty for this slot, which is computed
        from the weights of each tile. We use here the simplified
        entropy definition and we apply a random noise to avoid
        having to break ties.
        """
        if self.collapsed: return float('inf')  # Maybe this doesn't make sense, should be checked
        return np.log(self.sumOfWeights) - (self.sumOfWeightsLogs) / self.sumOfWeights + self.noise

    def remove_pattern(self, pattern, frequency_hints):
        # Remove pattern from possibility space.
        self.possibilities[pattern.index] = False

        # This is the relative frequency of the pattern.
        frequency = frequency_hints[pattern.index]

        # Update the entropy to maintain its computation constant.
        self.sumOfWeights -= frequency
        self.sumOfWeightsLogs -= np.log(frequency ** 2)

    def choose_pattern(self, fh):
        # Sample the uniform distribution
        sample = np.random.randint(self.sumOfWeights)

        # Filter possible tiles
        # print(len(self.possibilities))
        # print(len(self.patterns))
        possible = []
        for p in self.patterns:
            if self.possibilities:
                possible.append(p)
                
        # possible = [p for p in self.patterns if self.possibilities[p.index]]
        
        # Build a cummulative sum to sample from
        s = 0
        cummulativeFrequencies = [] 
        for p in self.patterns:
            s += fh[p.index]
            cummulativeFrequencies.append(s) 

        # Use binary search to get what pattern will be rendered
        index = np.searchsorted(self.cummulativeFrequencies, sample)

        return possible[index].index
