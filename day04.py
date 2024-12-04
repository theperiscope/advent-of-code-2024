with open("day04.txt", "r", encoding="utf-8") as f:
    g = [list(line.strip()) for line in f.readlines()]


# within the grid for each X, find all following, M, A, S and valid neighbors is any horizontal, vertical or diagonal
def find_xmas_sequences(g):
    directions, sequences = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)], []

    def is_valid(x, y):
        return 0 <= x < len(g) and 0 <= y < len(g[0])

    def find_sequence(x, y):
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and g[nx][ny] == "M":
                nnx, nny = nx + dx, ny + dy
                if is_valid(nnx, nny) and g[nnx][nny] == "A":
                    nnnx, nnnny = nnx + dx, nny + dy
                    if is_valid(nnnx, nnnny) and g[nnnx][nnnny] == "S":
                        sequences.append([(x, y), (nx, ny), (nnx, nny), (nnnx, nnnny)])

    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] == "X":
                find_sequence(i, j)

    return sequences


def find_mas_sequences(g):
    # within each 3x3 subgrid, center is A and corners (TL, BL, TR, BR order) are either MMSS, SMSM, SSMM, or MSMS
    patterns, sequences = [["M", "M", "S", "S"], ["S", "M", "S", "M"], ["S", "S", "M", "M"], ["M", "S", "M", "S"]], []

    def is_valid(x, y):
        return 0 <= x < len(g) and 0 <= y < len(g[0])

    for i in range(1, len(g) - 1):
        for j in range(1, len(g[0]) - 1):
            if g[i][j] == "A":
                corners = [g[i - 1][j - 1], g[i + 1][j - 1], g[i - 1][j + 1], g[i + 1][j + 1]]
                if corners in patterns:
                    sequences.append([(i - 1, j - 1), (i + 1, j - 1), (i - 1, j + 1), (i + 1, j + 1)])

    return sequences


print("Part 1", len(find_xmas_sequences(g)))
print("Part 2", len(find_mas_sequences(g)))
