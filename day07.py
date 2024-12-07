from itertools import product
import math


def read_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    result = {}
    for line in lines:
        target, value = line.split(": ")
        # interesting: in Python 3 int is unbounded
        result[int(target)] = list(map(int, value.strip().split(" ")))

    return result


def concatenate_numbers(a, b):
    # shorter version: return f"{a}{b}" but this avoids using string ops
    # --
    # no string ops version
    # num_digits = 0
    # x = b
    # while x > 0:
    #     x //= 10
    #     num_digits += 1
    # return a * (10**num_digits) + b
    # --
    # interesting: log10-based version of counting digits
    return a * (10 ** (math.floor(math.log10(b)) + 1)) + b


def check(target, numbers, include_concat=False):
    operators = ["+", "*"]
    if include_concat:
        operators.append("||")

    # https://docs.python.org/3/library/itertools.html#itertools.product
    for ops in product(operators, repeat=len(numbers) - 1):
        result = numbers[0]
        for n, op in zip(numbers[1:], ops):
            if op == "+":
                result += n
            elif op == "*":
                result *= n
            elif op == "||":
                result = concatenate_numbers(result, n)
        if result == target:
            return True
    return False


# __main__ is the name of the scope in which top-level code executes.
# https://docs.python.org/3/library/__main__.html
if __name__ == "__main__":
    filename = "day07.txt"
    data = read_file(filename)

    sum1, sum2 = 0, 0
    for target, numbers in data.items():
        if check(target, numbers):
            sum1 += target

    print("Part 1:", sum1)

    for target, numbers in data.items():
        if check(target, numbers, True):
            sum2 += target

    print("Part 2:", sum2)
