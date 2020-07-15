import random
import logging
from functools import reduce

import numpy as np

from wfc.utils import dirs, in_range


class Entropy:
    def __init__(self, weights, patterns):
        self.sow = sum(weights)
        self.sowl = sum(map(lambda p: weights[p.index] * np.log(weights[p.index]), patterns))
        self.noise = random.random() / 1e5

    @property
    def entropy(self):
        return np.log(self.sow) - self.sowl / self.sow + self.noise

    def __lt__(self, other):
        return self.entropy < other.entropy

    def __str__(self):
        return str(self.entropy)

    def __repr__(self):
        return self.__str__()


def wfc(patterns, valid, output_size):
    n, m = output_size

    # There are N * M uncollapsed slots (the size of the grid)
    # at the beginning.
    uncollapsed_count = n * m

    # How likely a given module is to appear in any slot.
    weights = [pattern.count for pattern in patterns]

    # AC3 consistency set.
    consistency_set = set()

    # Resulting grid.
    grid = np.array([[-1 for _ in range(m)] for _ in range(n)])

    # What patterns can be collapsed in a given position
    wave = np.array([[[True for _ in range(len(patterns))] for _ in range(m)] for _ in range(n)])

    # This is the uncertainty for this slot, which is computed
    # from the weights of each tile. We use here the simplified
    # entropy definition and we apply a random noise to avoid
    # having to break ties.
    # For now we'll use a matrix to store entropies.
    entropies = np.array([[Entropy(weights, patterns) for _ in range(m)] for _ in range(n)])

    def remove_pattern(pos, identifier):
        i, j = pos
        if wave[i][j][identifier]:
            # Remove pattern from possibility space.
            wave[i][j][identifier] = False

            # This is the relative frequency of the pattern.
            frequency = weights[identifier]

            # Update the entropy to maintain its computation constant.
            entropy = entropies[i][j]
            entropy.sow -= frequency
            entropy.sowl -= frequency * np.log(frequency)

    # Get the slot with the least entropy.
    def observe():
        minimum = float('inf')
        min_pos = (0, 0)
        for i in range(n):
            for j in range(m):
                if sum(wave[i][j]) > 1:
                    entropy = entropies[i][j].entropy
                    if entropy < minimum:
                        minimum = entropy
                        min_pos = (i, j)

        return min_pos

    def collapse(pos):
        nonlocal uncollapsed_count
        x, y = pos

        # Sample the uniform distribution
        f = []
        for pattern in filter(lambda p: wave[x][y][p.index], patterns):
            for _ in range(weights[pattern.index]):
                f.append(pattern.index)

        identifier = random.choice(f)

        # The slot is now collapsed.
        grid[x][y] = identifier

        # Since we locked in a pattern, remove all
        # other possibilities.
        wave[x][y] = [False for _ in range(len(patterns))]
        wave[x][y][identifier] = True

        # Schedule slot for a consistency update.
        consistency_set.add((x, y))

        # 1 less uncollapsed slot.
        uncollapsed_count -= 1

    def propagate():
        while consistency_set:
            x, y = consistency_set.pop()

            # Get the possible patterns for the origin.
            origin_domain = [index for index, is_possible in enumerate(wave[x][y]) if is_possible]

            # Check each of the adjacent slots.
            for d in dirs:
                dx, dy = d

                # This slot is outside of the output grid borders.
                if not in_range((x + dx, y + dy), grid):
                    continue

                # For each possible pattern of the origin, get its compatible
                # patterns in direction `d` and join them in a set.
                origin_domains_union = reduce(lambda a, b: a | valid(d, b), origin_domain, set())

                # Get the possible patterns for the neighbor in direction `d`.
                neighbor_domain = [index for index, is_possible in enumerate(wave[x + dx][y + dy]) if is_possible]

                # Each pattern in the neighbouring domain that doesn't exist in the
                # union must be removed, that way constraints propagate properly.
                removed = False
                for neighbor_id in neighbor_domain:
                    if neighbor_id not in origin_domains_union:
                        remove_pattern((x + dx, y + dy), neighbor_id)

                        possibility_count = sum(wave[x + dx][y + dy])
                        # There are no more possibilities: Contradiction.
                        if not possibility_count:
                            return False

                        # We may collapse this cell.
                        if possibility_count == 1:
                            collapse((x + dx, y + dy))
                            break

                        removed = True

                # Schedule slot for a consistency update if any pattern was removed.
                if removed:
                    consistency_set.add((x + dx, y + dy))

        # Propagated correctly.
        return True

    def generate(allowed_contradictions=10):
        if allowed_contradictions < 0:
            print("Max allowed contradictions reached.")

        propagated = True
        while propagated and uncollapsed_count:
            collapse(observe())
            propagated = propagate()
            yield grid, wave

        if not propagated:
            print("Contradiction")

        return generate(allowed_contradictions - 1)

    return grid, generate
