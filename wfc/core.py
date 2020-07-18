import random
import numpy as np

from functools import reduce
from wfc.entropy import Entropy
from wfc.extraction import dirs


def wfc(patterns, valid, output_size):
    n, m = output_size

    # There are N * M uncollapsed slots (the size of the grid)
    # at the beginning.
    uncollapsed_count = n * m

    # How likely a given module is to appear in any slot.
    weights = [pattern.count for pattern in patterns]

    # AC3 consistency stack.
    consistency_stack = []

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

        assert wave[i][j][identifier]

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
        i, j = pos

        # Sample the uniform distribution
        f = []
        for pattern in filter(lambda p: wave[i][j][p.index], patterns):
            for _ in range(weights[pattern.index]):
                f.append(pattern.index)

        identifier = random.choice(f)

        # The slot is now collapsed.
        grid[i][j] = identifier

        # Since we locked in a pattern, remove all
        # other possibilities.
        wave[i][j] = [False for _ in range(len(patterns))]
        wave[i][j][identifier] = True

        assert sum(wave[i][j]) > 0
        # Schedule slot for a consistency update.
        consistency_stack.append((i, j))

        # 1 less uncollapsed slot.
        uncollapsed_count -= 1

    def propagate():
        while consistency_stack:
            x, y = consistency_stack.pop()

            # Get the possible patterns for the origin.
            origin_domain = [index for index, is_possible in enumerate(wave[x][y]) if is_possible]

            # Check each of the adjacent slots.
            for d in dirs:
                dx, dy = d

                # This slot is outside of the output grid borders
                # or
                # a very key thing to notice: when we relax constraints, patterns
                # may appear collapsed where they were not supposed to, so
                # we need to allow anything to be collapsed or we might
                # create a contradiction on purpose (which is what we're doing).

                if not (0 <= x + dx < n and 0 <= y + dy < m) or sum(wave[x + dx][y + dy]) == 1:
                    continue

                # For each possible pattern of the origin, get its compatible
                # patterns in direction `d` and join them in a set.
                origin_domains_union = reduce(lambda a, b: a | valid(d, b), origin_domain, set())

                # Get the possible patterns for the neighbor in direction `d`.
                neighbor_domain = [index for index, is_possible in enumerate(wave[x + dx][y + dy]) if is_possible]

                # Each pattern in the neighbouring domain that doesn't exist in the
                # union must be removed, that way constraints propagate properly.
                for neighbor_id in neighbor_domain:
                    if neighbor_id not in origin_domains_union:
                        remove_pattern((x + dx, y + dy), neighbor_id)

                        possibility_count = sum(wave[x + dx][y + dy])

                        # print(possibility_count)
                        # There are no more possibilities: Contradiction.
                        if possibility_count < 1:
                            return False

                        # We may collapse this cell.
                        if possibility_count == 1:
                            collapse((x + dx, y + dy))
                            break

                        # Schedule slot for a consistency update if any pattern was removed.
                        consistency_stack.append((x + dx, y + dy))

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
