from collections import Counter

f = open("day01.txt", "r", encoding="utf-8")
lines = f.readlines()
f.close()

list1 = []
list2 = []

# split each line of two integers as two lists
for line in lines:
    num1, num2 = map(int, line.split())
    list1.append(num1)
    list2.append(num2)

# sort the two lists
list1.sort()
list2.sort()

# subtract list1 from list2
# https://docs.python.org/3/library/functions.html#zip
list3 = [abs(x - y) for x, y in zip(list2, list1)]

# sum list3
part1 = sum(list3)
print("part1", part1)

# how many times each number appears in list2
# https://docs.python.org/3/library/collections.html#collections.Counter
counter = Counter(list2)

# sum of n * counter[n] for n in list1
part2 = sum(n * counter[n] for n in list1)
print("part2", part2)
