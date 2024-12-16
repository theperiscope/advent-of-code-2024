from collections import defaultdict
from heapq import heappush, heappop
import sys
from typing import List, Tuple, Set
from PIL import Image, ImageDraw, ImageFont


def dijkstra(
    # interesting: Python types
    grid: List[str],
    start: Tuple[int, int],
    end: Tuple[int, int],
    initial_direction: str,
) -> Tuple[int, List[List[Tuple[int, int, str]]], Set[Tuple[int, int]]]:
    rows, cols = len(grid), len(grid[0])

    directions = {
        "^": (0, -1),
        "v": (0, 1),
        ">": (1, 0),
        "<": (-1, 0),
    }

    MOVE_COST, TURN_COST = 1, 1000

    def is_valid(x: int, y: int) -> bool:
        return 0 <= y < rows and 0 <= x < cols and grid[y][x] != "#"

    def get_turn_cost(current_dir: str, new_dir: str) -> int:
        return 0 if current_dir == new_dir else TURN_COST

    # priority queue for Dijkstra's algorithm: include the visited points set in the state to track complete paths
    initial_path_points = {start}  # Include start point

    # 0 is the initial cost
    pq = [(0, start, initial_direction, [(start[0], start[1], initial_direction)], initial_path_points)]

    # visited state: (position + direction)
    visited_states = set()

    # track minimum costs to reach each state
    costs = defaultdict(lambda: sys.maxsize)  # callable that returns sys.maxsize (maximum cost) for new states
    costs[(start, initial_direction)] = 0

    # store all optimal paths and their costs
    optimal_paths = []
    min_cost = sys.maxsize
    all_optimal_points = set()

    while pq:
        current_cost, current_pos, current_dir, path, path_points = heappop(pq)

        if current_cost > min_cost:
            continue

        if current_pos == end:
            path_points.add(end)  # Make sure to include end point
            if current_cost < min_cost:
                min_cost = current_cost
                optimal_paths = [path]
                all_optimal_points = path_points.copy()
            elif current_cost == min_cost:
                optimal_paths.append(path)
                all_optimal_points.update(path_points)
            continue

        state = (current_pos, current_dir)
        if state in visited_states and costs[state] < current_cost:
            continue

        visited_states.add(state)

        # try all directions
        for new_dir, (dx, dy) in directions.items():
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            new_pos = (new_x, new_y)

            if not is_valid(new_x, new_y):
                continue

            new_cost = current_cost + MOVE_COST + get_turn_cost(current_dir, new_dir)
            if new_cost > min_cost:
                continue

            new_state = (new_pos, new_dir)

            # allow re-visiting states if we have an equal cost path
            if new_cost <= costs[new_state]:
                costs[new_state] = new_cost
                new_path = path + [(new_x, new_y, new_dir)]
                # Create new set with all points in this path
                new_path_points = path_points.copy()
                new_path_points.add(new_pos)
                heappush(pq, (new_cost, new_pos, new_dir, new_path, new_path_points))

    if optimal_paths:
        return min_cost, optimal_paths, all_optimal_points

    return -1, [], set()


def save_maze_as_png(grid: List[str], filename: str, scale: int = 20) -> None:
    rows = len(grid)
    cols = len(grid[0])

    img = Image.new("RGBA", (cols * scale, rows * scale), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("lucon.ttf", 16)  # Lucida Console font

    colors = {
        "#": (33, 36, 47, 255),
        ".": (240, 240, 240, 0),
        "^": (210, 109, 152, 255),
        "v": (210, 109, 152, 255),
        "<": (210, 109, 152, 255),
        ">": (210, 109, 152, 255),
        "S": (20, 111, 221, 255),
        "E": (20, 111, 221, 255),
    }

    # nicer arrows
    arrows = {
        "S": "S",
        "E": "E",
        "^": "\u2191",
        "v": "\u2193",
        "<": "\u2190",
        ">": "\u2192",
        ".": "\u2022",
    }

    for y in range(rows):
        for x in range(cols):
            cell, x0, y0, x1, y1 = grid[y][x], x * scale, y * scale, (x + 1) * scale, (y + 1) * scale

            draw.rectangle([x0, y0, x1, y1], fill=colors[cell])

            if cell == "#":  # don't draw text of walls
                continue

            box = draw.textbbox((x0, y0), arrows[cell], font=font)
            fill_color = (66, 66, 66, 255) if cell == "." else (230, 230, 230, 255)
            draw.text(
                (x0 + (scale - (box[2] - box[0])) // 2, y0),
                arrows[cell],
                fill=fill_color,
                font=font,
            )

    img.save(filename, "PNG")


def print_optimal_paths(grid: List[str], optimal_paths: List[List[Tuple[int, int, str]]], visited: Set[Tuple[int, int]]) -> None:
    grid = [list(row) for row in grid]

    # mark all visited points with '.'
    for x, y in visited:
        if grid[y][x] not in {"S", "E"}:  # don't overwrite start and end
            grid[y][x] = "."

    # overlay the optimal path(s) points with arrows (show the last arrow direction)
    for path in optimal_paths:
        for x, y, arrow in path[1:-1]:  # except start and end
            grid[y][x] = arrow

    # print the grid using terminal colors
    for row in grid:
        for cell in row:
            if cell in "^v<>":
                print(f"\033[31;42m{cell}\033[0m", end="")
            elif cell == ".":
                print(f"\033[90m{cell}\033[0m", end="")
            elif cell == "#":
                print(f"\033[90;100m{cell}\033[0m", end="")
            elif cell in "SE":
                print(f"\033[101m{cell}\033[0m", end="")
            else:
                print(cell, end="")
        print()

    save_maze_as_png(grid, "day16.png")


def main():
    with open("day16.txt") as f:
        maze = [line.strip() for line in f]

    # Find start and end positions
    start = end = None
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)

    total_cost, optimal_paths, points_on_optimal_paths = dijkstra(maze, start, end, "E")

    if total_cost != -1:
        print("Part 1:", total_cost)
        print("Part 2:", len(points_on_optimal_paths))
        print_optimal_paths(maze, optimal_paths, points_on_optimal_paths)
    else:
        print("No path.")


# interesting: one way to call a main function in Python
if __name__ == "__main__":
    main()
