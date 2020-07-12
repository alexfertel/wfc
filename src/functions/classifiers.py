from src.pattern import Pattern


def deterministic():
    pattern_set = set()

    def classify(pattern):
        pat = Pattern(pattern)

        for p in pattern_set:
            if p == pat:
                p.count += pat.count
                return p
        else:
            pat.index = len(pattern_set)

        pattern_set.add(pat)

        return pat

    return classify, pattern_set
