with open("day25.txt", "r", encoding="UTF-8") as f:
    locks, keys = [], []
    for section in f.read().strip().split("\n\n"):
        (locks if section.startswith("#####") else keys).append({i for i, c in enumerate(section) if c == "#"})

    # if intersection of lock & key sets is empty, then there is no overlap
    print("Part 1:", sum(not lock & key for lock in locks for key in keys))
