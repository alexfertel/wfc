import numpy as np
from wfc.pattern import Pattern


def deterministic(ppatterns):
    pattern_set = []

    count = 0

    def classify(pattern):
        nonlocal count

        for p in pattern_set:
            if p == pattern:
                pat = p.copy()
                pat.count += 1
                break
        else:
            pattern_set.append(pattern)
            pattern.index = count
            count += 1

        return pattern

    for pp in ppatterns:
        classify(pp)

    return classify, pattern_set
