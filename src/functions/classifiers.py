from src.pattern import Pattern


def deterministic():
    pattern_set = set()

    def classify_pattern(pattern):
        pat = Pattern(pattern)

        for p in pattern_set:
            if p == pat:
                p.count += pat.count
        else:
            pat.index = len(pattern_set)

        pattern_set.add(pat)

    return pattern_set, classify_pattern
