from collections import defaultdict
import math


def blink(map):
    new_map = defaultdict(int)
    for N, count in map.items():
        digits = 1 if N == 0 else math.floor(math.log10(N)) + 1
        if N == 0:
            new_map[1] += count
        elif digits % 2 == 0:
            left, right = divmod(N, 10 ** (digits // 2))  # interesting: divmod returns tuple of quotient and remainder
            # two statements consecutively because left and right can be same
            new_map[left] += count
            new_map[right] += count
        else:
            new_map[N * 2024] += count
    return new_map


with open("day11.txt", encoding="utf-8") as f:
    numbers_map = defaultdict(int, {n: 1 for n in map(int, f.read().strip().split())})

for i in range(75):
    numbers_map = blink(numbers_map)
    if i in {24, 74}:
        print(f"Part {1 if i == 24 else 2}:", sum(numbers_map.values()))
