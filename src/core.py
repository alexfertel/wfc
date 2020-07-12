import numpy as np

from functools import reduce

from .slot import Slot
from .utils import dirs, in_range


class Core:
    def __init__(
            self,
            patterns,
            weights,
            valid,
            size):

        # List of NxN submatrices.
        self.patterns = patterns

        # Size of the output matrix.
        self.output_size = (0, 0)

        # Initialize necessary fields.
        self.reset()

        # How likely a given module is to appear in any slot.
        self.weights = weights

        # Look-up table to use
        self.valid = valid

        # Output grid.
        self.output = None

    def reset(self):
        """
        The `Core` class is left in a known state, 
        the same as when initializing the class.
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

        # Update the internal state of the slot
        slot.update(index)

        # Schedule slot for a consistency update.
        self.stack.append((x, y))

        # 1 less uncollapsed slot.
        self.uncollapsed_count -= 1

        # Update this slot's entropy.
        self.entropies[x][y] = slot.entropy

    def propagate(self):
        while self.stack:
            x, y = self.stack.pop()
            triggering_slot = self.grid[x][y]

            # Get the possible patterns for the triggering_slot.
            ting_slot_patterns = [
                p for p in triggering_slot.patterns if triggering_slot.possibilities[p.index]]

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
                ted_slot_patterns = [
                    p for p in triggered_slot.patterns if triggered_slot.possibilities[p.index]]

                # Union of the spaces.
                space = ting_slot_patterns

                def check_validity(pattern):
                    return self.valid(d, pattern.index)

                domains_union = reduce(lambda a, b: a | check_validity(b), space, set())

                # For each pattern of the triggered slot, check if
                # that pattern has the possibility of appearing,
                # which is an existence check in the union of domains.
                for triggered in ted_slot_patterns:
                    if triggered.index not in domains_union:
                        triggered_slot.remove_pattern(triggered, self.weights)

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
        sowl = sum([self.weights[p.index] * np.log(self.weights[p.index])
                    for p in self.patterns])

        # Populate the grid with slots.
        for i in range(n):
            for j in range(m):
                s = Slot((i, j), self.patterns, sow, sowl)

                # Update the grid.
                self.grid[i][j] = s

                # Update the entropy.
                self.entropies[i][j] = s.entropy

    def generate(self, size, ground=0, allowed_contradictions=10):
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
