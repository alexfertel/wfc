from collections import defaultdict
from pprint import pprint

from .pattern import Pattern
from .slot import Slot
from .utils import dirs, render, compatible

import numpy as np
import time

class WFC:
    def __init__(self, allow_rotations=False, allow_reflections=False):
        self.patterns = []
        self.adjacency_rules = defaultdict(list)
        
        # How likely a given module is to appear in any slot.
        self.weights = []
        # self.p2i = {}
        # self.i2p = {}

        self.restart()

        self.allow_rotations = allow_rotations
        self.allow_reflections = allow_reflections

    # Preprocess input image to extract patterns, compute frequency hints
    # and build adjacency rules.
    def preprocess(self, example, n):
        matrix = np.array(example)  # Let's work with numpy

        # Extract patterns without wrapping.
        self.patterns = self.extract_patterns(matrix, n)

        # Learn adjacencies
        for p1 in self.patterns:
            for p2 in self.patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1, p2, d):
                        self.adjacency_rules[(p1.index, d)].append(p2.index)
                        self.adjacency_rules[(p2.index, (-x, -y))].append(p1.index)

                    # self.adjacency_rules[(p1.index, p2.index, d)] = compatible(p1, p2, d)

                    # # Maybe this isn't needed.
                    # self.adjacency_rules[(p2.index, p1.index, (-d[0], -d[1]))] = compatible(p2, p1, (-d[0], -d[1]))

        # for item in self.patterns:
        #    pprint(item.matrix) 
        # pprint(self.adjacency_rules)


    def extract_patterns(self, matrix, size):
        n, m = matrix.shape

        submatrices = []
        for i in range(n - size + 1):
            for j in range(m - size + 1):
                sm = matrix[i: i + size, j: j + size]
                submatrices.append(sm)

                # Add rotations. We argue reflections
                # and rotations should be allowed not always
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


    def run(self, size, max_contradictions_allowed=10):
        x, y = size

        if max_contradictions_allowed < 0:
            return np.zeros(size)

        self.restart()

        # So ugly! T_T
        self.init_grid(size)

        # There are N * M uncollapsed slots (the size of the grid)
        # at the beginning.
        self.uncollapsed_count = x * y
        propagated = True
        while propagated and self.uncollapsed_count:
            # time.sleep(1)
            # pprint(self.entropies)
            # for row in self.entropies:
            #     print(row)

            # Retrieve the cell with the minimum entropy
            # print(len(self.heap))
            # s = hq.heappop(self.heap)
            s = self.observe()

            # Collapse the slot
            self.collapse(s.pos)
            
            # pprint(self.grid)
            propagated = self.propagate()

            snapshot = []
            for row in self.grid:
                sr = []
                for slot in row:
                    sr.append(slot.color)
                snapshot.append(sr)
            self.history.append(snapshot)



        if not propagated:
            pprint(self.grid)
            print("Contradiction")
        return render(self.grid) if propagated else self.run(size, max_contradictions_allowed - 1)

    def init_grid(self, size):
        x, y = size

        self.grid = [[0 for _ in range(y)] for _ in range(x)]
        self.entropies = np.ones(size)
        
        sow = sum(self.weights)
        sowl = sum([self.weights[p.index] * np.log(self.weights[p.index]) for p in self.patterns])

        # Populate the grid with slots
        for i in range(x):
            for j in range(y):
                s = Slot((i, j), self.patterns, sow, sowl)

                # Update the grid
                self.grid[i][j] = s

                # Update the entropy
                self.entropies[i][j] = s.entropy
    
    def propagate(self):
        # TODO: Maybe use setdiff
        while self.stack:
            x, y = self.stack.pop()
            triggering_slot = self.grid[x][y]

            # Iterate over every slot that
            # may have patterns in common with 
            # latest collapsed slot
            # print(x, y, dx, dy)


            # Get the possible patterns for the triggering_slot
            ps1 = [p for p in triggering_slot.patterns if triggering_slot.possibilities[p.index]]

            for d in dirs:
                dx, dy = d
                if not self.in_range((x + dx, y + dy)):
                    continue

                triggered_slot = self.grid[x + dx][y + dy]

                if triggered_slot.collapsed:
                    continue

                # Get the possible patterns for the triggered_slot
                ps2 = [p for p in triggered_slot.patterns if triggered_slot.possibilities[p.index]]

                domains = []
                for p1 in ps1:
                    domains.extend(self.adjacency_rules[p1.index, d])


                for p2 in ps2:
                    if not p2.index in domains:
                        triggered_slot.remove_pattern(p2, self.weights)

                        if not sum(triggered_slot.possibilities):
                            return False
                        
                        # We may collapse this cell
                        if sum(triggered_slot.possibilities) == 1:
                            self.collapse(triggered_slot.pos)
                            break

                        self.stack.append((x + dx, y + dy))


                self.entropies[x + dx][y + dy] = triggered_slot.entropy

        return True

    def observe(self):
        index = np.argmin(self.entropies)
        i, j = np.unravel_index(index, self.entropies.shape)
        slot = self.grid[i][j]
        return slot

    def validate_adjacency(self, i1, i2, d):
        return i2 in self.adjacency_rules[(i1, d)]

    def restart(self):
        # Resulting grid
        # TODO: Include it as a parameter?
        self.grid = []

        # This is the entropy heap. This will return the 
        # slot with the minimum entropy.
        # self.heap = []

        # # For now we'll use a matrix to store entropies
        # self.entropies = np.array()

        # This is the forward checking stack
        self.stack = []

        # # When this is zero, we finished generating
        # self.uncollapsed_count = 0

        self.history = []

    def in_range(self, pos):
        x, y = pos
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])


