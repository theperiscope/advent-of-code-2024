from collections import defaultdict
from itertools import pairwise


def next(n):
    n ^= (n << 6) & 0xFFFFFF  # 2^24 is 16777216, and MOD equals & with 0xFFFFFF
    n ^= (n >> 5) & 0xFFFFFF
    n ^= (n << 11) & 0xFFFFFF
    return n


with open("day22.txt") as f:
    input = map(int, f.read().strip().splitlines())

part1, part2_patterns = 0, defaultdict(int)
for n in input:
    secret_numbers = [n] + [n := next(n) for _ in range(2000)]  # interesting: walrus operator, := assigns values to variables
    part1 += secret_numbers[-1]

    differences = [b % 10 - a % 10 for a, b in pairwise(secret_numbers)]  # interesting: second time pairwise is useful

    seen_patterns = set()
    for i in range(len(secret_numbers) - 4):
        pattern = tuple(differences[i : i + 4])
        if pattern not in seen_patterns:
            part2_patterns[pattern] += secret_numbers[i + 4] % 10
            seen_patterns.add(pattern)

print("Part 1:", part1)

part2 = max(part2_patterns.values())
print("Part 2:", part2)
