from collections import Counter
import numpy as np
import heapq as hq

# 4-neighbourhood
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Pattern:
    def __init__(self, matrix, index):
        self.matrix = matrix
        self.index = index
    
    @property
    def color(self):
        return self.matrix[0][0]
    
class Slot:
    def __init__(self, pos):
        self.pos = pos

        # This is used when rendering the slot.
        self.color = None

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
        noise = np.random.ranf() / 1e5

        # Wether the cell is collapsed or not. A heap of the slots is
        # kept in order to quickly retrieve the slot with the minimum
        # entropy, each time a slot's entropy varies, we push it into 
        # the heap, resulting in the possibility of having the same
        # slot in the heap, thus needing to know if a cell is collapsed
        # when popping it from the heap.
        self.collapsed = False

        # This is used when propagating a pattern selection for
        # a given slot. 
        self.tile_enabler_counts = [[len(self.patterns) for _ in dirs] for _ in self.patterns]


    # Make the set of slots a lattice.
    def __lt__(self, other):
        return self.entropy < other.entropy
    
    @property
    def entropy(self)
        """
        This is the uncertainty for this slot, which is computed
        from the weights of each tile. We use here the simplified
        entropy definition and we apply a random noise to avoid
        having to break ties.
        """
        if self.collapsed: return 0  # Maybe this doesn't make sense, should be checked
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
        sample = np.randint(self.sumOfWeights)

        # Filter possible tiles
        possible = [p for p in self.patterns if self.possibilities[i]]
        
        # Build a cummulative su tosamplefrom that
        s = 0
        cummulativeFrequencies = [] 
        for p in self.patterns:
            s += fh[p.index]
            cummulativeFrequencies.append(s) 

        # Use binary search to get what pattern will be rendered
        index = np.searchsorted(self.cummulativeFrequencies, sample)

        return possible[index].index

class WFC:
    def __init__(self):
        self.patterns = []
        self.adjacency_rules = {}
        
        # How likely a given module is to appear in any slot.
        self.frequency_hints = Counter()
        self.p2i = {}
        self i2p = {}

        # Resulting grid
        # TODO: Include it as a parameter?
        self.grid = []

        # This is the entropy heap. This will return the 
        # slot with the minimum entropy.
        self.heap = []

        # This is the forward checking stack
        self.stack = []

    # Preprocess input image to extract patterns, compute frequency hints
    # and build adjacency rules.
    def preprocess(self, example, n):
        matrix = np.array(example)  # Let's work with numpy

        # Extract patterns without wrapping.
        self.patterns = extract_patterns(example, n)

        # Learn adjacencies
        for p1, p2 in zip(self.patterns, self.patterns):
            for d in dirs:
                self.adjacency_rules[(p1, p2, d)] = compatible(p1, p2, d)

                # Maybe this isn't needed.
                self.adjacency_rules[(p2, p1, -d)] = compatible(p2, p1, -d)


    def extract_patterns(self, matrix, size):
        n, m = matrix.shape

        submatrices = []
        for i in range(n - size + 1):
            for j in range(m - size + 1):
                pat = Pattern(matrix[i: i + size, j: j + size])
                pat.index = len(submatrices)
                self.frequency_hints[pat.index] += 1
                submatrices.append(pat)

        return submatrices

    
    def collapse(self, pos):
        x, y = pos

        slot = self.grid[x][y]
        index = slot.choose_pattern(self.frequency_hints)

        # TODO:
        # Since we chose a pattern to lock, should we do
        # this inside `choose_pattern`? I don't think
        # we call `choose_pattern` anywhere else.
        slot.collapsed = True

        # Since we locked in a pattern, remove all
        # other possibilities.
        # slot.possibilities = [False for i, p in enumerate(slot.possibilities) if i != index]
        slot.possibilities = [False for p in self.patterns if p.index != index]

        # Update the color of the slot
        slot.color = self.patterns[index].color

        # for dx, dy in dirs:
        #     self.stack.append((self.grid[x + dx][y + dy], -(dx, dy)))
        self.stack.append(((x, y), index))
        
    def run(self, size):
        x, y = size
        
        init_grid(grid)

        # Retrieve the cell with the minimum entropy
        s = hp.heappop(self.heap)

        # Collapse the slot
        self.collapse(s.pos)
        
        self.propagate()


    def init_grid(self):
        self.grid = np.empty(size)
        
        sow = sum(self.frequency_hints.values())
        sowl = sum([self.frequency_hints[p.index] * np.log(self.frequency_hints[p.index]) for p in self.patterns])

        # Populate the grid with slots
        for i in range(x):
            for j in range(y):
                s = Slot()
                s.pos = (i, j)
                s.possibilities = [True for _ in self.patterns]
                s.patterns = self.patterns
                s.sumOfWeights = sow
                s.sumOfWeightsLogs = sowl

                self.grid[i][j] = s

                # Push the slot to the heap
                hp.heappush(self.heap, s)
    
    def propagate(self):
        # """
        # Initially the stack has four elements, which are the neighbours 
        # of the collapsed slot. 
        # """
        """
        Initially, the stack has one element which is the first collapsed
        slot in this iteration of the algorithm.
        """

        while self.stack:
            # Get the top of the stack
            (x, y), pat_index = self.stack.pop()

            for dx, dy in dirs:
                



            # if not in_range(slot.pos) or slot.collapsed:
            #     continue

            
            
            

    def in_range(self, pos):
        x, y = pos
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])


def compatible(p1, p2, d):
    return matrix_lap(p1, d) == matrix_lap(p2, -d)


def matrix_lap(matrix, direction):
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


