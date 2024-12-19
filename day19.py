from functools import cache


def read_file(filename):
    with open(filename, "r") as f:
        content = f.read().strip().split("\n\n")
    return content[0].split(", "), content[1].split("\n")


towel_patterns, desired_designs = read_file("day19.txt")  # similar to chunk & words


def is_possible(desired_design, memoize=None):
    if memoize is None:
        memoize = {}

    if len(desired_design) == 0:
        return 1

    if desired_design not in memoize:
        memoize[desired_design] = sum(
            is_possible(desired_design[len(p) :], memoize) for p in towel_patterns if desired_design.startswith(p)
        )

    return memoize[desired_design]


@cache  # interesting: equivalent to memoization, https://docs.python.org/3/library/functools.html#functools.cache
def is_possible_2(desired_design):
    return len(desired_design) == 0 or sum(
        is_possible_2(desired_design.removeprefix(p)) for p in towel_patterns if desired_design.startswith(p)
    )


part1 = sum(1 for d in desired_designs if is_possible(d) > 0)
part1a = sum(1 for d in desired_designs if is_possible_2(d) > 0)
print("Part 1:", part1, part1a)

part2 = sum(is_possible(d) for d in desired_designs)
part2a = sum(is_possible_2(d) for d in desired_designs)
print("Part 2:", part2, part2a)
