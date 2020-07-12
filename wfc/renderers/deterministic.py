class DeterministicRenderer:
    def __init__(self, patterns):
        super().__init__()

        self.patterns = patterns

    def render_patterns(self, identifiers):
        n, m = identifiers.shape

        rendered = [[-1 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                rendered[i][j] = self.patterns[identifiers[i][j]].matrix[0][0]

        return rendered
