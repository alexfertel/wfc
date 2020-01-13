import numpy as np

from collections import defaultdict
from functools import reduce
from pprint import pprint

from .pattern import Pattern
from .slot import Slot
from .utils import dirs, compatible, in_range
from .classifiers.deterministic import DeterministicClassifier
from .validators.deterministic import DeterministicValidator


class Core:
    def __init__(
            self, 
            example, 
            size, 
            classifier=None,
            validator=None,
            # renderer,
            allow_rotations=False, 
            allow_reflections=False):

        # This is the example image.
        self.example = np.array(example)

        # This is the N for the NxN patterns.
        self.size = size

        # Size of the output matrix.
        self.output_size = (0, 0)

        self.allow_rotations = allow_rotations
        self.allow_reflections = allow_reflections

        # Initialize necessary fields.
        self.reset()

        # How likely a given module is to appear in any slot.
        self.weights = []

        # Setup `Classifier` instance.
        self.classifier = classifier if classifier else DeterministicClassifier()

        # Preprocess input image to extract patterns, compute frequency hints
        # and build adjacency rules.
        # Extract patterns without wrapping.
        self.classify_patterns()
        print("Done setting up classifier.")

        # Setup `Validator` instance.
        self.validator = validator if validator else DeterministicValidator(self.patterns)
        print("Done setting up validator.")

        # Output grid.
        self.output = None


    def reset(self):
        """
        This functions leaves the `Core` class in a
        known state, the same as when initializing the class.
        """
        # Size of the ouput
        x, y = self.output_size

        # Resulting grid.
        self.grid = [[0 for _ in range(y)] for _ in range(x)]

        # This is the forward checking stack
        # Maybe it's AC3, TODO: check this.
        self.stack = []
        
        # For now we'll use a matrix to store entropies.
        # TODO: Check if using a heap is reasonable.
        self.entropies = np.ones(self.output_size)

        return self

    def extract_patterns(self):
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

        return submatrices

    def classify_patterns(self):
        patterns = self.extract_patterns()

        patterns, weights = self.classifier.classify_patterns(patterns)

        self.patterns = patterns
        self.weights = weights

        return self

    def observe(self):
        # Get the slot with the least entropy.
        index = np.argmin(self.entropies)

        # Map the 1d index to 2d.
        i, j = np.unravel_index(index, self.entropies.shape)

        # Retrieve slot.
        slot = self.grid[i][j]

        return slot

    def collapse(self, pos):
        x, y = pos

        slot = self.grid[x][y]
        index = slot.choose_pattern(self.weights)

        # The slot is now collapsed.
        slot.collapsed = True

        # Since we locked in a pattern, remove all
        # other possibilities.
        for p in self.patterns:
            if p.index != index:
                slot.possibilities[p.index] = False

        # Update the color of the slot.
        slot.color = self.patterns[index].color

        # Update selected pattern
        slot.identifier = index

        # Schedule slot for a consistency update.
        self.stack.append((x, y))
        
        # 1 less uncollapsed slot.
        self.uncollapsed_count -= 1

        # Update this slot's entropy.
        self.entropies[x][y] = slot.entropy

    def propagate(self):
        # TODO: Maybe use setdiff
        while self.stack:
            x, y = self.stack.pop()
            triggering_slot = self.grid[x][y]

            # Get the possible patterns for the triggering_slot.
            ting_slot_patterns = [p for p in triggering_slot.patterns if triggering_slot.possibilities[p.index]]

            # Check each of the adjacent slots.
            for d in dirs:
                dx, dy = d

                # This slot is outside of the output grid borders.
                if not in_range((x + dx, y + dy), self.grid):
                    continue
                
                triggered_slot = self.grid[x + dx][y + dy]

                # This slot is already collapsed, so there's nothing to propagate.
                if triggered_slot.collapsed:
                    continue

                # Get the possible patterns for the triggered_slot.
                ted_slot_patterns = [p for p in triggered_slot.patterns if triggered_slot.possibilities[p.index]]

                # Union of the spaces.
                domains_union = []
                for allowed_pat in ting_slot_patterns:
                    domains_union = np.union1d(domains_union, self.validator.valid_adjacencies(allowed_pat.index, d))

                # For each pattern of the triggered slot, check if
                # that pattern has the possibility of appearing,
                # which is a check of existence in the union of domains. 
                for p2 in ted_slot_patterns:
                    if not p2.index in domains_union:
                        triggered_slot.remove_pattern(p2, self.weights)

                        # There are no more possibilities: Contradiction.
                        if not sum(triggered_slot.possibilities):
                            return False
                        
                        # We may collapse this cell.
                        if sum(triggered_slot.possibilities) == 1:
                            self.collapse(triggered_slot.pos)
                            break

                        # Schedule slot for a consistency update.        
                        self.stack.append((x + dx, y + dy))

                # Update entropies.
                self.entropies[x + dx][y + dy] = triggered_slot.entropy

        # Propagated correctly.
        return True

    def initialize_output_matrix(self, size):
        n, m = size

        sow = sum(self.weights)
        sowl = sum([self.weights[p.index] * np.log(self.weights[p.index]) for p in self.patterns])
        
        # Populate the grid with slots.
        for i in range(n):
            for j in range(m):
                s = Slot((i, j), self.patterns, sow, sowl)

                # Update the grid.
                self.grid[i][j] = s

                # Update the entropy.
                self.entropies[i][j] = s.entropy

    def generate(self, size, allowed_contradictions=10):
        x, y = self.output_size = size

        if allowed_contradictions < 0:
            print("Max allowed contradictions reached.")

        self.reset()
        self.initialize_output_matrix(size)
        print("Done initializing output matrix.")

        # There are N * M uncollapsed slots (the size of the grid)
        # at the beginning.
        self.uncollapsed_count = x * y
        propagated = True
        while propagated and self.uncollapsed_count:
            # Compute the slot with the minimum entropy.
            s = self.observe()
            # print("Observed")

            # Collapse the slot.
            self.collapse(s.pos)
            # print("Collapsed")
            
            # Propagate consistency.
            propagated = self.propagate()
            # print("Propagated")

            # Yield current assignment.
            yield self.grid

        if not propagated:
            print("Contradiction")

        return self.generate(size, allowed_contradictions - 1)


