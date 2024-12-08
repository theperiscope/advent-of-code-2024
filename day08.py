from itertools import combinations
from collections import defaultdict


def read_file(filename):
    antenna_locations = defaultdict(list)
    with open(filename, "r", encoding="utf-8") as f:
        grid = [list(line.strip()) for line in f.readlines()]
        rows, cols = len(grid) - 1, len(grid[0]) - 1
        for row, line in enumerate(grid):
            for col, char in enumerate(line):
                if char != ".":
                    antenna_locations[char].append((row, col))

    return (grid, antenna_locations, rows, cols)


if __name__ == "__main__":
    grid, antenna_locations, rows, cols = read_file("day08.txt")
    for antenna, locations in antenna_locations.items():
        for loc1, loc2 in combinations(locations, 2):
            # 2-antenna distance as list of number of [rows, cols]
            d = [abs(loc2[0] - loc1[0]), abs(loc2[1] - loc1[1])]

            if loc1[0] > loc2[0] and loc1[1] > loc2[1]:
                p1, p2 = (loc1[0] + d[0], loc1[1] + d[1]), (loc2[0] - d[0], loc2[1] - d[1])
            elif loc1[0] > loc2[0] and loc1[1] < loc2[1]:
                p1, p2 = (loc1[0] + d[0], loc1[1] - d[1]), (loc2[0] - d[0], loc2[1] + d[1])
            elif loc1[0] < loc2[0] and loc1[1] > loc2[1]:
                p1, p2 = (loc1[0] - d[0], loc1[1] + d[1]), (loc2[0] + d[0], loc2[1] - d[1])
            else:
                p1, p2 = (loc1[0] - d[0], loc1[1] - d[1]), (loc2[0] + d[0], loc2[1] + d[1])

            # Part 2: continue line with p1, then p2, until out-of-bounds
            while 0 <= p1[0] <= rows and 0 <= p1[1] <= cols:
                grid[p1[0]][p1[1]] = "#"

                # calculate new p1 + D based on loc1 and loc2
                if loc1[0] > loc2[0] and loc1[1] > loc2[1]:
                    p1 = (p1[0] + d[0], p1[1] + d[1])
                elif loc1[0] > loc2[0] and loc1[1] < loc2[1]:
                    p1 = (p1[0] + d[0], p1[1] - d[1])
                elif loc1[0] < loc2[0] and loc1[1] > loc2[1]:
                    p1 = (p1[0] - d[0], p1[1] + d[1])
                else:
                    p1 = (p1[0] - d[0], p1[1] - d[1])

            while 0 <= p2[0] <= rows and 0 <= p2[1] <= cols:
                grid[p2[0]][p2[1]] = "#"

                # calculate new p2 + D based on loc1 and loc2
                if loc1[0] > loc2[0] and loc1[1] > loc2[1]:
                    p2 = (p2[0] - d[0], p2[1] - d[1])
                elif loc1[0] > loc2[0] and loc1[1] < loc2[1]:
                    p2 = (p2[0] - d[0], p2[1] + d[1])
                elif loc1[0] < loc2[0] and loc1[1] > loc2[1]:
                    p2 = (p2[0] + d[0], p2[1] - d[1])
                else:
                    p2 = (p2[0] + d[0], p2[1] + d[1])

    count_hash = sum(line.count("#") for line in grid)
    count_non_dot = sum(1 for line in grid for char in line if char != ".")

    print("\n".join("".join(line) for line in grid) + "\n")
    print(f"Part 1: {count_hash} (count '#' characters)")
    print(f"Part 2: {count_non_dot} (total number of non-'.' characters)")
