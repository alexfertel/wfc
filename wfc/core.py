import numpy as np

from functools import reduce

from wfc.slot import Slot
from wfc.utils import dirs, in_range


def wfc(patterns, valid, output_size):
    n, m = output_size

    # There are N * M uncollapsed slots (the size of the grid)
    # at the beginning.
    uncollapsed_count = n * m

    # How likely a given module is to appear in any slot.
    weights = [pattern.count for pattern in patterns]

    # This is the forward checking stack
    # Maybe it's AC3, TODO: check this out.
    stack = []

    sow = sum(weights)
    sowl = sum(map(lambda p: weights[p.index] * np.log(weights[p.index]), patterns))

    # Resulting grid.
    grid = [[Slot((i, j), patterns, sow, sowl) for j in range(m)] for i in range(n)]

    # For now we'll use a matrix to store entropies.
    # TODO: Check if using a heap is reasonable.
    entropies = np.ones(output_size)

    # Populate the grid with slots.
    for i in range(n):
        for j in range(m):
            # Update the entropy.
            entropies[i][j] = grid[i][j].entropy

    def observe():
        # Get the slot with the least entropy.
        index = np.argmin(entropies)

        # Map the 1d index to 2d.
        x, y = np.unravel_index(index, entropies.shape)

        # Retrieve slot.
        slot: Slot = grid[x][y]

        return slot

    def collapse(pos):
        nonlocal uncollapsed_count
        x, y = pos

        slot: Slot = grid[x][y]
        index = slot.choose_pattern(weights)

        # Update the internal state of the slot
        slot.update(index)

        # Schedule slot for a consistency update.
        stack.append((x, y))

        # 1 less uncollapsed slot.
        uncollapsed_count -= 1

        # Update this slot's entropy.
        entropies[x][y] = slot.entropy

    def propagate():
        while stack:
            x, y = stack.pop()
            triggering_slot = grid[x][y]

            # Get the possible patterns for the triggering_slot.
            ting_slot_patterns = [
                p for p in triggering_slot.patterns if triggering_slot.possibilities[p.index]]

            # Check each of the adjacent slots.
            for d in dirs:
                dx, dy = d

                # This slot is outside of the output grid borders.
                if not in_range((x + dx, y + dy), grid):
                    continue

                triggered_slot = grid[x + dx][y + dy]

                # This slot is already collapsed, so there's nothing to propagate.
                if triggered_slot.collapsed:
                    continue

                # Get the possible patterns for the triggered_slot.
                ted_slot_patterns = [
                    p for p in triggered_slot.patterns if triggered_slot.possibilities[p.index]]

                # Union of the spaces.
                space = ting_slot_patterns

                def check_validity(pattern):
                    return valid(d, pattern.index)

                domains_union = reduce(lambda a, b: a | check_validity(b), space, set())

                # For each pattern of the triggered slot, check if
                # that pattern has the possibility of appearing,
                # which is an existence check in the union of domains.
                for triggered in ted_slot_patterns:
                    if triggered.index not in domains_union:
                        triggered_slot.remove_pattern(triggered, weights)

                        # There are no more possibilities: Contradiction.
                        if not sum(triggered_slot.possibilities):
                            return False

                        # We may collapse this cell.
                        if sum(triggered_slot.possibilities) == 1:
                            collapse(triggered_slot.pos)
                            break

                        # Schedule slot for a consistency update.
                        stack.append((x + dx, y + dy))

                # Update entropies.
                entropies[x + dx][y + dy] = triggered_slot.entropy

        # Propagated correctly.
        return True

    def generate(allowed_contradictions=10):
        if allowed_contradictions < 0:
            print("Max allowed contradictions reached.")

        propagated = True
        while propagated and uncollapsed_count:
            slot: Slot = observe()
            collapse(slot.pos)
            propagated = propagate()
            yield grid

        if not propagated:
            print("Contradiction")

        return generate(allowed_contradictions - 1)

    return grid, generate
