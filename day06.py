f = open("day06.txt", "r", encoding="utf-8")
data_map = [line.strip() for line in f.readlines()]
f.close()


def find_start(data_map):
    for row_index, row in enumerate(data_map):
        if "^" in row:
            return row_index, row.index("^")
    return -1, -1


def move_and_mark(data_map, start_row, start_col, extra_wall_row=None, extra_wall_col=None):
    rows, cols = len(data_map), len(data_map[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
    dir_index = 0
    direction = directions[dir_index]

    visited = set()
    row, col = start_row, start_col
    while 0 <= row < rows and 0 <= col < cols:
        if (row, col, dir_index) in visited:
            return None
        visited.add((row, col, dir_index))

        next_row, next_col = row + direction[0], col + direction[1]

        if (0 <= next_row < rows and 0 <= next_col < cols and data_map[next_row][next_col] == "#") or (
            extra_wall_row is not None and extra_wall_col is not None and next_row == extra_wall_row and next_col == extra_wall_col
        ):
            dir_index = (dir_index + 1) % 4  # turn right
            direction = directions[dir_index]
            continue
        else:
            data_map[row] = data_map[row][:col] + "X" + data_map[row][col + 1 :]
            row, col = next_row, next_col
        if not (0 <= row < rows and 0 <= col < cols):
            break

    return data_map


start_row, start_col = find_start(data_map)
data_map = move_and_mark(data_map, start_row, start_col)

for line in data_map:
    print(line)

count_X = sum(row.count("X") for row in data_map)
print("Part 1:", count_X)

# Part 2 is brute-forced, about 35 seconds
rows, cols, loop_count = len(data_map), len(data_map[0]), 0

for row in range(rows):
    for col in range(cols):
        if data_map[row][col] != "#":
            result_map = move_and_mark(data_map, start_row, start_col, row, col)
            if result_map is None:
                loop_count += 1
                continue

print("Part 2:", loop_count)
