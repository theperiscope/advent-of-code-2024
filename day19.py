def read_file(filename):
    with open(filename, "r") as f:
        content = f.read().strip().split("\n\n")
    return content[0].split(", "), content[1].split("\n")


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


towel_patterns, desired_designs = read_file("day19.txt")  # similar to chunk & words

part1 = sum(1 for d in desired_designs if is_possible(d) > 0)
print(f"Part 1: {part1}")

part2 = sum(is_possible(d) for d in desired_designs)
print(f"Part 2: {part2}")
