from collections import Counter
from pprint import pprint

from .pattern import Pattern
from .slot import Slot
from .utils import dirs, render

import numpy as np
import heapq as hq
import time

class WFC:
    def __init__(self):
        self.patterns = []
        # self.adjacency_rules = {}
        
        # How likely a given module is to appear in any slot.
        self.weights = []
        # self.p2i = {}
        # self.i2p = {}

        self.restart()

    # Preprocess input image to extract patterns, compute frequency hints
    # and build adjacency rules.
    def preprocess(self, example, n):
        matrix = np.array(example)  # Let's work with numpy

        # Extract patterns without wrapping.
        self.patterns = self.extract_patterns(matrix, n)

        # Learn adjacencies
        # for p1, p2 in zip(self.patterns, self.patterns):
        #     for d in dirs:
                # self.adjacency_rules[(p1, p2, d)] = compatible(p1, p2, d)

                # Maybe this isn't needed.
                # self.adjacency_rules[(p2, p1, -d)] = compatible(p2, p1, -d)


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
                    sm = np.rot90(sm)
                    submatrices.append(sm)

        unique, counts = np.unique(submatrices, return_counts=True, axis=0)
        patterns = [Pattern(pat, index) for index, pat in enumerate(unique)]

        self.weights = np.array(counts)

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
        slot.possibilities = [False for p in self.patterns if p.index != index]

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

        # There are N * M uncollapsed cells (the size of the grid)
        # at the beginning.
        self.uncollapsed_count = x * y
        propagated = True
        while propagated and self.uncollapsed_count:
            # time.sleep(1)
            # pprint(self.entropies)
            # Retrieve the cell with the minimum entropy
            # print(len(self.heap))
            # s = hq.heappop(self.heap)
            s = self.observe()

            # Collapse the slot
            self.collapse(s.pos)
            
            # pprint(self.grid)
            propagated = self.propagate()


        if not propagated:
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
                s = Slot((i, j))
                # s.pos = (i, j)
                s.possibilities = [True for _ in self.patterns]
                s.patterns = self.patterns
                s.sumOfWeights = sow
                s.sumOfWeightsLogs = sowl

                self.grid[i][j] = s

                # Update the entropy
                self.entropies[i][j] = s.entropy

                # Push the slot to the heap
                # hq.heappush(self.heap, s)

    
    def propagate(self):
        while self.stack:
            x, y = self.stack.pop()
            (dx, dy) = pattern_size = self.patterns[0].matrix.shape
            # collapsed_slot = self.grid[x][y]

            # Iterate over every slot that
            # may have patterns in common with 
            # latest collapsed slot
            # print(x, y, dx, dy)
            for i in range(x - dx + 1, x + 1):
                for j in range(y - dy + 1, y + 1):
                    # If it is out of the grid, ignore.
                    # If it has already been collapsed, ignore
                    if not self.in_range((i, j)):
                        continue

                    slot = self.grid[i][j]

                    if slot.collapsed:
                        continue
                    
                    # For each pattern in the possibility space
                    # of this slot, try fitting it here, which
                    # means (matching it with the current collapsed
                    # slots on the grid) seeing if it matches with
                    # the recently collapsed slot.
                    
                    possibilities_count = sum(slot.possibilities)
                    for pattern in slot.patterns:
                        # print(pattern.matrix)
                        # print(i, j)
                        # print(dx, dy)
                        # print(pattern.matrix[x - i][y - j])
                        # print(slot.color)
                        # print(collapsed_slot.color)

                        if slot.possibilities[pattern.index]:
                            for n in range(dx):
                                for m in range(dy):
                                    if not self.in_range((i + n, j + m)):
                                        continue

                                    subslot = self.grid[i + n][j + m]

                                    if subslot.color == -1:
                                        continue

                                    if pattern.matrix[n][m] != subslot.color:
                                        slot.remove_pattern(pattern, self.weights)
                                        possibilities_count -= 1                            

                                        # Contradiction! We have to start again
                                        if not possibilities_count:
                                            self.restart()
                                            return False
                                            # raise Exception("Contradiction!")

                                        self.entropies[i][j] = slot.entropy


                        # if slot.possibilities[pattern.index] and pattern.matrix[x - i][y - j] != collapsed_slot.color:
                            # slot.remove_pattern(pattern, self.weights)
                            # possibilities_count -= 1                            

                            # # Contradiction! We have to start again
                            # if not possibilities_count:
                            #     self.restart()
                            #     return False
                            #     # raise Exception("Contradiction!")

                            # self.entropies[i][j] = slot.entropy
                            # new_patterns.append(pattern)
                        # else:
                            # slot.possibilities[pattern.index] = False
                    
                    # Update the possibility space removing the 
                    # patterns that would break the generation
                    # with sort of a forward checking algorithm.
                    # slot.patterns = new_patterns


                    # We may collapse this cell
                    if possibilities_count == 1:
                        self.collapse(slot.pos)                        

        return True

        # Update slot colors

    def observe(self):
        index = np.argmin(self.entropies)
        i, j = np.unravel_index(index, self.entropies.shape)
        slot = self.grid[i][j]
        return slot

            
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

    def in_range(self, pos):
        x, y = pos
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])


# def compatible(p1, p2, d):
#     return matrix_lap(p1, d) == matrix_lap(p2, -d)


# def matrix_lap(matrix, direction):
#     n, m = matrix.shape
    
#     if direction == (0, -1):  # North
#         return matrix[: -1, :]
#     if direction == (1, 0):  # East
#         return matrix[:, 1:]
#     if direction == (0, 1):  # South
#         return matrix[1:, :]
#     if direction == (-1, 0):  # West
#         return matrix[:, :-1]

#     return False

