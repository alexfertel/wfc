from src.pattern import Pattern


def upper_left_corner(pattern: Pattern):
    return pattern.matrix[0][0]


def center(pattern: Pattern):
    n, m = pattern.matrix.shape
    i, j = n // 2, m // 2
    return pattern.matrix[i][j]


def deterministic(patterns, color_extractor=center):
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
