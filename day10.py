def find_paths(grid, start, path, target):
    if not (0 <= start[0] < len(grid) and 0 <= start[1] < len(grid[0])):
        return []
    if grid[start[0]][start[1]] != target:
        return []
    if target == 9:
        if len(path) == 9:
            return [path + [start]]
        else:
            return []
    next_target = target + 1
    paths = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_start = (start[0] + dx, start[1] + dy)
        # interesting: extending list based on an iterable
        paths.extend(find_paths(grid, next_start, path + [start], next_target))
    return paths


def main():
    f = open("day10.txt", "r", encoding="utf-8")
    grid = []
    for row in f.readlines():
        # "." support is only for debugging more basic scenarios
        grid.append([int(char) if char != "." else -1 for char in row.strip()])
    f.close()

    zero_positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]
    nine_positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 9]

    part1, part2 = 0, 0
    for start in zero_positions:
        paths = find_paths(grid, start, [], 0)

        distinct_nine_positions = set()
        for path in paths:
            if path[-1] in nine_positions:
                distinct_nine_positions.add(path[-1])

        print(f"Distinct nine positions: {len(distinct_nine_positions)} ({distinct_nine_positions})")

        part1 += len(distinct_nine_positions)
        part2 += len(paths)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
