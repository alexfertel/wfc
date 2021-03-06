import random

import numpy as np


class Slot:
    def __init__(self, pos, patterns, sow, sowl):
        self.pos = pos

        # This is used when rendering the slot.
        self.color = -1

        # This is the possibility space of the slot.
        self.patterns = patterns

        # This masks the possibility space
        self.possibilities = [True for _ in self.patterns]

        # These properties aid when calculating entropy;
        # they are used to make entropy computation constant.
        self.sumOfWeights = sow
        self.sumOfWeightsLogs = sowl

        # Applying noise to the entropy, so we don't have to break ties.
        # Initialize a tiny random value.
        self.noise = random.random() / 1e5

        # Whether the cell is collapsed or not. A heap of the slots is
        # kept in order to quickly retrieve the slot with the minimum
        # entropy, each time a slot's entropy varies, we push it into
        # the heap, resulting in the possibility of having the same
        # slot in the heap, thus needing to know if a cell is collapsed
        # when popping it from the heap.
        self.collapsed = False

        # This will be used when rendering the slot. It is the identifier of
        # the pattern collapsed in this slot.
        self.identifier = -1

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
        if self.collapsed:
            # Maybe this doesn't make sense, should be checked
            return float('inf')
        return np.log(self.sumOfWeights) - self.sumOfWeightsLogs / self.sumOfWeights + self.noise

    def remove_pattern(self, pattern, weights):
        if self.possibilities[pattern.index]:
            # Remove pattern from possibility space.
            self.possibilities[pattern.index] = False

            # This is the relative frequency of the pattern.
            frequency = weights[pattern.index]

            # Update the entropy to maintain its computation constant.
            self.sumOfWeights -= frequency
            self.sumOfWeightsLogs -= frequency * np.log(frequency)

    def choose_pattern(self, weights):
        # Sample the uniform distribution
        p = []
        for pattern in self.patterns:
            if self.possibilities[pattern.index]:
                for _ in range(weights[pattern.index]):
                    p.append(pattern.index)

        return random.choice(p)

    def update(self, index):
        # The slot is now collapsed.
        self.collapsed = True

        # Since we locked in a pattern, remove all
        # other possibilities.
        for p in self.patterns:
            if p.index != index:
                self.possibilities[p.index] = False

        # Update the color of the slot.
        self.color = self.patterns[index].color

        # Update selected pattern
        self.identifier = index
