dirs = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}


def parse_input(grid_str):
    return [list(line) for line in grid_str.strip().split("\n")]


def find_robot(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                return (x, y)
    return None


def double_grid(grid):
    cell_map = {"#": "##", ".": "..", "@": "@.", "O": "[]"}
    return ["".join(cell_map[cell] for cell in row) for row in grid]


def can_push_boxes(grid, x, y, dx, dy):
    while True:
        next_x, next_y = x + dx, y + dy
        if not (0 <= next_x < len(grid[0]) and 0 <= next_y < len(grid)):  # we can't push if outside the grid
            return False
        cell = grid[next_y][next_x]
        if cell == ".":  # we can push the boxes only if there is a free space
            return True
        if cell == "#":  # we can't push the boxes if there is a wall
            return False
        if cell == "O":  # we can push multiple boxes simultaneously so continue to check
            x, y = next_x, next_y
            continue
        return False


def push_boxes(grid, x, y, dx, dy):
    boxes = []  # store all boxes to push
    curr_x, curr_y = x, y

    # find all boxes to push
    while True:
        next_x, next_y = curr_x + dx, curr_y + dy
        if grid[next_y][next_x] == ".":
            break
        if grid[next_y][next_x] == "O":
            boxes.append((next_x, next_y))
            curr_x, curr_y = next_x, next_y
        else:
            break

    # push boxes in reverse order to avoid overwriting
    for box_x, box_y in reversed(boxes):
        grid[box_y][box_x], grid[box_y + dy][box_x + dx] = ".", "O"


def move_part1(grid, x, y, dx, dy):
    new_x, new_y = x + dx, y + dy

    if not (0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid)):
        return (x, y)

    if grid[new_y][new_x] == "#":
        return (x, y)

    if grid[new_y][new_x] == ".":
        grid[y][x], grid[new_y][new_x] = ".", "@"
        return (new_x, new_y)

    if grid[new_y][new_x] == "O" and can_push_boxes(grid, new_x, new_y, dx, dy):
        push_boxes(grid, x, y, dx, dy)
        grid[y][x], grid[new_y][new_x] = ".", "@"
        return (new_x, new_y)

    return (x, y)


def solve(grid_str, moves):
    grid = parse_input(grid_str)
    x, y = find_robot(grid)

    for m in moves:
        if m in dirs:
            dx, dy = dirs[m]
            x, y = move_part1(grid, x, y, dx, dy)

    return sum(100 * y + x for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == "O")


grid_str, moves = open("day15.txt").read().split("\n\n")
print("Part 1:", solve(grid_str, moves))


grid_str = "\n".join(double_grid(parse_input(grid_str)))


def solve_part2(grid_str, moves):
    grid = parse_input(grid_str)
    x, y = find_robot(grid)

    for m in moves:
        if m in dirs:
            dx, dy = dirs[m]
            if move_part2(grid, x, y, dx, dy):
                x, y = (x + dx, y + dy)

    return sum(100 * y + x for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == "[")


def move_part2(grid, x, y, dx, dy):
    if not can_push_boxes2(grid, x, y, dx, dy):
        return False

    ps = [(x, y)]
    if dy != 0:
        if grid[y][x] == "[":  # for [ append the next cell so we have full [] box for what we are pushing
            ps.append((x + 1, y))
        elif grid[y][x] == "]":  # for ] append the previous cell so we have full [] box for what we are pushing
            ps.append((x - 1, y))

    for x, y in ps:
        nx, ny = (x + dx, y + dy)
        if grid[ny][nx] == ".":
            grid[y][x], grid[ny][nx] = grid[ny][nx], grid[y][x]  # swap
        elif grid[ny][nx] in "[]":
            move_part2(grid, nx, ny, dx, dy)  # recursively move the box
            grid[y][x], grid[ny][nx] = ".", grid[y][x]
    return True


def can_push_boxes2(grid, x, y, dx, dy):
    ps = [(x, y)]
    if dy != 0:
        if grid[y][x] == "[":  # for [ append the next cell so we have full [] box for what we are pushing
            ps.append((x + 1, y))
        elif grid[y][x] == "]":  # for ] append the previous cell so we have full [] box for what we are pushing
            ps.append((x - 1, y))

    for x, y in ps:
        nx, ny = x + dx, y + dy
        dest = grid[ny][nx]
        if dest == ".":  # continue if empty space
            continue
        elif dest == "#":  # we can't push the boxes if there is a wall
            return False
        elif dest in "[]":
            if not can_push_boxes2(grid, nx, ny, dx, dy):  # recursively check if we can push boxes from new position
                return False
    return True


print("Part 2:", solve_part2(grid_str, moves))
