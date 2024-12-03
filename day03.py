import re

f = open("day03.txt", "r", encoding="utf-8")
contents = f.read()
f.close()

matches = re.finditer(r"(mul)\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don\'t)\(\)", contents, re.MULTILINE)

part1 = 0
part2 = 0
doMul = True
for matchNum, match in enumerate(matches, start=1):
    if match.group() == "do()":
        doMul = True
        continue
    elif match.group() == "don't()":
        doMul = False
        continue

    # mul operation
    op = match.group(1)
    a = int(match.group(2))
    b = int(match.group(3))
    part1 += a * b
    part2 += a * b if doMul else 0

print("part1", part1)
print("part2", part2)
