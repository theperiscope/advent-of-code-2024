import sys
from heapq import heappop, heappush
from time import time
from utils import AocInput


def parse_grid(grid):
    flat_grid, width = "".join(grid), len(grid[0])  # interesting: fast way to find start and end by flattening
    S, E = flat_grid.find("S"), flat_grid.find("E")
    return (S // width, S % width), (E // width, E % width)


def create_distance_map(grid, start):
    distances, heap = {}, [(0, start)]

    while heap:
        d, current = heappop(heap)
        if current in distances:
            continue

        distances[current] = d
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] in ".SE" and (nx, ny) not in distances:
                heappush(heap, (d + 1, (nx, ny)))

    return distances


def count_shortcuts(grid, start, end, cheats_allowed=2):
    # Pre-compute all constant values
    start_distances = create_distance_map(grid, start)
    end_distances = create_distance_map(grid, end)
    base_length = start_distances[end]
    count, min_path_threshold = 0, base_length - 100
    w, h = len(grid[0]), len(grid)

    # optimization: pre-compute manhattan distance checks
    valid_offsets = [
        (dy, dx)
        for dy in range(-cheats_allowed, cheats_allowed + 1)
        for dx in range(-cheats_allowed, cheats_allowed + 1)
        if abs(dy) + abs(dx) <= cheats_allowed
    ]

    # optimization: use generator expression instead of nested loops
    for y, x in ((y, x) for y in range(h) for x in range(w) if grid[y][x] != "#"):
        path_to_start = start_distances.get((y, x), sys.maxsize)
        if path_to_start >= min_path_threshold:
            continue

        for dy, dx in valid_offsets:
            ey, ex = y + dy, x + dx
            if not (0 <= ey < h and 0 <= ex < w) or grid[ey][ex] == "#":
                continue

            min_possible_path = path_to_start + abs(dy) + abs(dx) + end_distances.get((ey, ex), sys.maxsize)
            if base_length - min_possible_path >= 100:
                count += 1

    return count


if __name__ == "__main__":
    aoc = AocInput()
    grid = aoc.get_input_lines(2024, 20)
    start_time = time()
    start, end = parse_grid(grid)

    for part, cheats in enumerate([2, 20], 1):
        result = count_shortcuts(grid, start, end, cheats)
        print(f"Part {part}:", result)

    total_time = time() - start_time
    print(f"Total time: {total_time:.2f}s")
