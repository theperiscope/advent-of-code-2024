f = open("day02.txt", "r", encoding="utf-8")
lines = f.readlines()
f.close()

part1 = 0
part2 = 0
for line in lines:
    # split line as integer list
    report = list(map(int, line.split()))

    # create list of differences between consequtive elements in the report
    diffs = [report[i + 1] - report[i] for i in range(0, len(report) - 1)]
    # print(diffs)

    # check if numbers are all positive and at most 3
    safe = all(0 < diff <= 3 for diff in diffs) or all(-3 <= diff < 0 for diff in diffs)
    # print(safe)

    if not safe:
        # try to remove one element and check if that makes report is safe
        for x in range(len(report)):
            new_report = report[:x] + report[x + 1 :]
            new_diffs = [new_report[i + 1] - new_report[i] for i in range(0, len(new_report) - 1)]
            new_safe = all(0 < diff <= 3 for diff in new_diffs) or all(-3 <= diff < 0 for diff in new_diffs)
            if new_safe:
                break

    part1 += 1 if safe else 0
    part2 += 1 if safe or new_safe else 0

print("part1", part1)
print("part2", part2)
