import numpy as np
from wfc.pattern import Pattern


def deterministic(ppatterns):
    pattern_set = []

    count = 0

    def classify(pattern):
        nonlocal count
        pat = Pattern(pattern)

        for p in pattern_set:
            if p == pat:
                pat = p.copy()
                pat.count += 1
                break
        else:
            pattern_set.append(pat)
            pat.index = count
            count += 1

        print(pat)
        return pat

    for pp in ppatterns:
        classify(pp)

    return classify, pattern_set
