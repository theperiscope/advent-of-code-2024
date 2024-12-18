from collections import deque


def get_neighbors(x, y, maze):
    return [
        (x + dx, y + dy)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if 0 <= y + dy < len(maze) and 0 <= x + dx < len(maze[0]) and maze[y + dy][x + dx] != "#"
    ]


def find_path_bfs(grid):
    end = (len(grid[0]) - 1, len(grid) - 1)
    queue = deque([(0, 0, 0)])  # x, y, distance
    visited = {(0, 0)}

    while queue:
        x, y, dist = queue.popleft()
        if (x, y) == end:
            return dist
        for nx, ny in get_neighbors(x, y, grid):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))
    return -1


def create_maze_grid(walls, size=71):
    grid = [["." for _ in range(size)] for _ in range(size)]
    for x, y in walls:
        if 0 <= x < size and 0 <= y < size:
            grid[y][x] = "#"
    return grid


def read_walls(filename="day18.txt"):
    with open(filename) as f:
        return [tuple(map(int, line.split(","))) for line in f if line.strip()]


def binary_search_blocking_wall(walls, start=1024, size=71):
    low, high = start, len(walls)
    while low < high:
        mid = (low + high) // 2
        if find_path_bfs(create_maze_grid(walls[:mid], size)) == -1:
            high = mid
        else:
            low = mid + 1
    return walls[low - 1]


if __name__ == "__main__":
    walls = read_walls()
    print("Part 1:", find_path_bfs(create_maze_grid(walls[:1024])))
    block_x, block_y = binary_search_blocking_wall(walls)
    print("Part 2:", f"{block_x},{block_y}")
