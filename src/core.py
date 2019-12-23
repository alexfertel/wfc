from collections import defaultdict
from pprint import pprint

from .pattern import Pattern
from .slot import Slot
from .utils import dirs, render, compatible

import numpy as np

class Core:
    def __init__(self, example, size, allow_rotations=False, allow_reflections=False):
        # This is the example image.
        self.example = np.array(example)

        # This is the N for the NxN patterns. 
        self.size = size

        # Initialize needed fields.
        self.reset()

        # Preprocess input image to extract patterns, compute frequency hints
        # and build adjacency rules.
        # Extract patterns without wrapping.
        self.patterns = self.clasify_patterns()

        self.learn_adjacencies()


    def reset(self):
        """
        This functions leaves the `Core` class in a
        known state, the same as when initializing the class.
        """
        # Resulting grid.
        self.grid = [[0 for _ in range(y)] for _ in range(x)]

        # This is the forward checking stack
        # Maybe it's AC3, TODO: check this.
        self.stack = []

        # This is the list of patterns from the example image.
        self.patterns = []

        # These are the adjacency rules learned from the example.
        self.adjacency_rules = defaultdict(list)
        
        # How likely a given module is to appear in any slot.
        self.weights = []

        # For now we'll use a matrix to store entropies.
        # TODO: Check if using a heap is reasonable.
        self.entropies = np.ones(self.size)

        return self

    def learn_adjacencies(self):
        # Learn adjacencies
        for p1 in self.patterns:
            for p2 in self.patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1, p2, d):
                        self.adjacency_rules[(p1.index, d)].append(p2.index)
                        self.adjacency_rules[(p2.index, (-x, -y))].append(p1.index)

        return self

    def clasify_patterns(self):
        n, m = self.example.shape
        N = self.size

        submatrices = []
        for i in range(n - N + 1):
            for j in range(m - N + 1):
                sm = self.example[i: i + N, j: j + N]
                submatrices.append(sm)

                # Add rotations. We argue reflections
                # and rotations should not be always allowed.
                for _ in range(3):
                    if self.allow_rotations:
                        sm = np.rot90(sm)
                        submatrices.append(sm)

                    if self.allow_reflections:
                        sm = np.flip(sm)
                        submatrices.append(sm)

        unique, counts = np.lib.arraysetops.unique(submatrices, return_counts=True, axis=0)
        patterns = [Pattern(pat, index) for index, pat in enumerate(unique)]

        self.weights = counts

        return patterns

    def collapse(self, pos):
        x, y = pos

        slot = self.grid[x][y]
        index = slot.choose_pattern(self.weights)

        # TODO:
        # Since we chose a pattern to lock, should we do
        # this inside `choose_pattern`? I don't think
        # we call `choose_pattern` anywhere else.
        slot.collapsed = True

        # Since we locked in a pattern, remove all
        # other possibilities.
        # slot.possibilities = [False for i, p in enumerate(slot.possibilities) if i != index]
        for p in self.patterns:
            if p.index != index:
                slot.possibilities[p.index] = False
        # slot.possibilities = [False for p in self.patterns if p.index != index]

        # Update the color of the slot
        slot.color = self.patterns[index].color

        # for dx, dy in dirs:
        #     self.stack.append((self.grid[x + dx][y + dy], -(dx, dy)))
        self.stack.append((x, y))
        
        self.uncollapsed_count -= 1

        # Update this slot's entropy
        self.entropies[x][y] = slot.entropy



    def initialize_output_matrix(self, size):
        n, m = size

        sow = sum(self.weights)
        sowl = sum([self.weights[p.index] * np.log(self.weights[p.index]) for p in self.patterns])

        # Populate the grid with slots
        for i in range(n):
            for j in range(m):
                s = Slot((i, j), self.patterns, sow, sowl)

                # Update the grid
                self.grid[i][j] = s

                # Update the entropy
                self.entropies[i][j] = s.entropy


    def generate(self, size, allowed_contradictions=10):
        if allowed_contradictions < 0:
            print("Max allowed contradictions reached.")

        self.reset()
        self.initialize_output_matrix(size)

        # There are N * M uncollapsed slots (the size of the grid)
        # at the beginning.
        self.uncollapsed_count = x * y
        propagated = True
        while propagated and self.uncollapsed_count:
            # Compute the slot with the minimum entropy
            s = self.observe()

            # Collapse the slot
            self.collapse(s.pos)
            
            # Propagate consistency
            propagated = self.propagate()

            # Yield current assignment
            yield self.grid

        if not propagated:
            print("Contradiction")

        return self.generate(size, allowed_contradictions - 1)


