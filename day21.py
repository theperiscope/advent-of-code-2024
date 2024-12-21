from itertools import pairwise, permutations
from functools import cache

MOVES = {"<": (-1, 0), ">": (1, 0), "v": (0, 1), "^": (0, -1)}


@cache  # 25-level recursion is too much without memoization
def get_distance_xy(a, b):
    if a == b:
        return 0, 0

    # choose keypad type and convert index positions to (x,y) coordinates
    keypad = "X^A<v>" if any(c in "<>v^" for c in (a + b)) else "789456123X0A"
    ax, ay = keypad.index(a) % 3, keypad.index(a) // 3
    bx, by = keypad.index(b) % 3, keypad.index(b) // 3
    return bx - ax, by - ay


@cache
def is_valid_path(a, b, path):
    # choose keypad type and convert starting position to coordinates
    keypad = "X^A<v>" if any(c in "<>v^" for c in (a + b)) else "789456123X0A"
    ax, ay = keypad.index(a) % 3, keypad.index(a) // 3

    # follow the path to the end and perform checks along the way
    for p in path:
        dx, dy = MOVES[p]
        ax, ay = ax + dx, ay + dy
        if ax < 0 or ax >= 3 or ay < 0 or ay >= len(keypad) // 3:
            return False
        if keypad[ay * 3 + ax] == "X":
            return False
    return True


@cache
def get_all_paths(a, b):
    dx, dy = get_distance_xy(a, b)

    # determine required directional moves
    cx = "<" if dx < 0 else ">"
    cy = "^" if dy < 0 else "v"

    # create string of required moves (not necessarily correct yet)
    moves = f"{cx * abs(dx)}{cy * abs(dy)}"

    possible = []
    for move_permutation in permutations(moves):
        # quick check if we need to move right and up for example, any path starting with down or left is invalid
        # we don't have to wait for is_valid_path to consider as not possible
        if (
            (dx > 0 and move_permutation[0] == "<")
            or (dx < 0 and move_permutation[0] == ">")
            or (dy > 0 and move_permutation[0] == "^")
            or (dy < 0 and move_permutation[0] == "v")
        ):
            continue

        if is_valid_path(a, b, move_permutation):
            possible.append("".join(move_permutation) + "A")

    return possible


@cache
def get_min_button_presses(sequence, depth):  # return minimum number of button presses required
    N = 0
    sequence = "A" + sequence  # start from position A

    # we are dialing sequence in order (i.e. 029A) - so we analyze each pair of consecutive positions
    for a, b in pairwise(sequence):  # interesting: pairwise generates pairs of consecutive elements
        all_valid_paths = get_all_paths(a, b)
        if depth == 0:
            # base case: use shortest path length
            N += min(len(path) for path in all_valid_paths)
        else:
            # recursive case: optimize path further
            N += min(get_min_button_presses(path, depth - 1) for path in all_valid_paths)
    return N


def solve(sequences, depth):
    return sum(get_min_button_presses(s, depth) * int(s[:-1]) for s in sequences)  # remove last character (A) before multiplying


if __name__ == "__main__":
    with open("day21.txt") as f:
        sequences = f.read().splitlines()

    print("Part 1:", solve(sequences, 2))
    print("Part 2:", solve(sequences, 25))
