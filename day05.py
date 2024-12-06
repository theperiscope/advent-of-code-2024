"""
The sample input can be represent as a directed graph. Here's a Mermaid diagram of the graph:

```mermaid
graph TD;

29 --> 13
47 --> 13
47 --> 29
47 --> 53
47 --> 61
53 --> 13
53 --> 29
61 --> 13
61 --> 29
61 --> 53
75 --> 13
75 --> 29
75 --> 47
75 --> 53
75 --> 61
97 --> 13
97 --> 29
97 --> 47
97 --> 53
97 --> 61
97 --> 75
```
"""

from collections import defaultdict

section1, section2 = open("day05.txt").read().split("\n\n")
updates = [list(map(int, line.split(","))) for line in section2.splitlines()]
print(updates)

page_before_rules = defaultdict(list)
for r in section1.split("\n"):
    before, after = r.split("|")
    page_before_rules[int(before)].append(int(after))
print(page_before_rules)

part1 = 0
part2 = 0
for list_of_page_numbers in updates:
    print("---")
    print(list_of_page_numbers)
    # sort pages by the number of rules that contain each page that is in the pages list (descending)
    sorted_list_of_page_numbers = sorted(
        list_of_page_numbers, key=lambda p: -len([x for x in page_before_rules[p] if x in list_of_page_numbers])
    )
    print(sorted_list_of_page_numbers)
    # if the sorted page numbers are the same as the original page numbers after the sort we have part 1
    if list_of_page_numbers == sorted_list_of_page_numbers:
        part1 += list_of_page_numbers[len(list_of_page_numbers) // 2]
    # otherwise, the sort result will show the way they should've been ordered/given (part 2)
    else:
        part2 += sorted_list_of_page_numbers[len(sorted_list_of_page_numbers) // 2]

print("Part 1", part1)
print("Part 2", part2)
