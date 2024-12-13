import re

with open("day13.txt", "r", encoding="UTF-8") as f:
    data = f.read().strip().split("\n\n")

input, pattern = [], re.compile(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")

for block in data:
    match = pattern.match(block)
    if match:
        ax, ay, bx, by, px, py = map(int, match.groups())
        input.append({"ax": ax, "ay": ay, "bx": bx, "by": by, "px": px, "py": py})

part1 = part2 = 0
for entry in input:
    # Part 1, interesting: solve using Cramer’s Rule for Solving a System of Two Equations
    # Cramer is better here because inverted matrix-based approach is float-heavy and can produce rounding errors
    # https://pressbooks.bccampus.ca/algebraintermediate/chapter/solve-systems-of-equations-using-determinants/

    # matrix determinant formula: det = ax * by - bx * ay
    det = entry["ax"] * entry["by"] - entry["bx"] * entry["ay"]
    # calculate det_x determinant after replacing the first column of the matrix with the solution column
    det_x = entry["px"] * entry["by"] - entry["bx"] * entry["py"]
    # calculate det_y determinant after replacing the second column of the matrix with the solution column
    det_y = entry["ax"] * entry["py"] - entry["px"] * entry["ay"]
    # solution will be x=dx/det, y=dy/det
    (a_presses, rem_a), (b_presses, rem_b) = divmod(det_x, det), divmod(det_y, det)

    # our solution must have whole numbers that are >= 0
    if a_presses >= 0 and b_presses >= 0 and rem_a == rem_b == 0:
        part1 += 3 * a_presses + 1 * b_presses

    # Part 2, modifies the entry px/py
    entry["px"], entry["py"] = entry["px"] + 10_000_000_000_000, entry["py"] + 10_000_000_000_000

    # re-calculate det_x and det_y for the new x, y values
    det_x = entry["px"] * entry["by"] - entry["bx"] * entry["py"]
    det_y = entry["ax"] * entry["py"] - entry["px"] * entry["ay"]
    # re-calculate our solution
    (a_presses, rem_a), (b_presses, rem_b) = divmod(det_x, det), divmod(det_y, det)

    # our solution must have whole numbers that are >= 0
    if a_presses >= 0 and b_presses >= 0 and rem_a == rem_b == 0:
        part2 += 3 * a_presses + 1 * b_presses

print("Part 1:", part1)
print("Part 2:", part2)
