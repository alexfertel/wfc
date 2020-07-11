def color_from_pattern(pattern):
    return pattern.matrix[0][0]


def deterministic(patterns, color_extractor=color_from_pattern):
    def render(grid):
        n, m = grid.shape

        rendered = [[-1 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                identifier = grid[i][j].identifier
                color = color_extractor(patterns[identifier])
                rendered[i][j] = color

        return rendered

    return render
