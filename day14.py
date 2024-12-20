from PIL import Image
import random

with open("day14.txt", "r", encoding="UTF-8") as f:
    data = f.read().strip().split("\n\n")

# parse input data
robots = []
for line in data:
    for robot in line.split("\n"):
        p, v = robot.split(" v=")
        px, py = map(int, p[2:].split(","))
        vx, vy = map(int, v.split(","))
        robots.append({"position": (px, py), "velocity": (vx, vy)})

board_size_w, board_size_h = 101, 103
if len(robots) <= 12:  # sample input variation
    board_size_w, board_size_h = 11, 7

middle_x, middle_y = board_size_w // 2, board_size_h // 2


# part 1
for i in range(100):
    for robot in robots:
        px, py = robot["position"]
        vx, vy = robot["velocity"]
        new_x = (px + vx) % board_size_w
        new_y = (py + vy) % board_size_h
        robot["position"] = (new_x, new_y)

quadrant_counts = [0, 0, 0, 0]
for robot in robots:
    x, y = robot["position"]
    if y != middle_y and x != middle_x:
        quadrant_counts[(x > middle_x) + 2 * (y > middle_y)] += 1

product_of_counts = 1
for count in quadrant_counts:
    product_of_counts *= count

print("Part 1:", product_of_counts)

if len(robots) <= 12:
    print("Program can only run Part 1 for the sample input data. Use full input data for Part 2 solution and visualization.")
    exit()


def create_board(board_size_w, board_size_h, robots=None):
    board = ["." * board_size_w for _ in range(board_size_h)]
    if robots:
        board = [list(row) for row in board]
        for robot in robots:
            x, y = robot["position"]
            if 0 <= x < board_size_w and 0 <= y < board_size_h:
                board[y][x] = "#"
        board = ["".join(row) for row in board]
    return board


part2 = 0
board = []
for i in range(99999):
    for robot in robots:
        px, py = robot["position"]
        vx, vy = robot["velocity"]
        new_x = (px + vx) % board_size_w
        new_y = (py + vy) % board_size_h
        robot["position"] = (new_x, new_y)

    board = create_board(board_size_w, board_size_h, robots)

    if any("##########" in row for row in board):
        part2 = i + 1
        break

print("Part 2:", part2)


# interesting: Github Copilot suggested this function to save the board as a .png image
def save_board_as_image(board, filename):
    height, width, transparent, red, green = len(board), len(board[0]), (255, 255, 255, 0), (255, 58, 47, 255), (12, 176, 74, 255)
    image = Image.new("RGBA", (width * 10, height * 10), transparent)
    pixels = image.load()

    # interesting: circle pattern tool https://donatstudios.com/PixelCircleGenerator
    def draw_circle(pixels, cx, cy, color):
        pattern = [
            "...####...",
            ".########.",
            ".########.",
            "##########",
            "##########",
            "##########",
            "##########",
            ".########.",
            ".########.",
            "...####...",
        ]
        for py in range(10):
            for px in range(10):
                if pattern[py][px] == "#":
                    px_scaled = cx + px - 5
                    py_scaled = cy + py - 5
                    if 0 <= px_scaled < width * 10 and 0 <= py_scaled < height * 10:
                        pixels[px_scaled, py_scaled] = color

    for y in range(height):
        for x in range(width):
            if board[y][x] == "#":
                color = random.choice([red, green])
                draw_circle(pixels, x * 10 + 10 // 2, y * 10 + 10 // 2, color)

    image.save(filename)


# just for fun: save the board as a .png image
save_board_as_image(board, "christmas-tree.png")
print("Image saved as 'christmas-tree.png'")
