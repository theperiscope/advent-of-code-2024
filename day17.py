def run(program, a=0, b=0, c=0):
    ip, output = 0, []
    while ip < len(program) - 1:
        opcode, operand = program[ip], program[ip + 1]
        combo = operand if operand < 4 else [a, b, c][operand - 4]
        match opcode:
            case 0:  # adv
                a, ip = a // (2**combo), ip + 2
            case 1:  # bxl
                b, ip = b ^ operand, ip + 2
            case 2:  # bst
                b, ip = combo % 8, ip + 2
            case 3:  # jnz
                ip = operand if a != 0 else ip + 2
            case 4:  # bxc
                b, ip = b ^ c, ip + 2
            case 5:  # out
                output.append(combo % 8)
                ip += 2
            case 6:  # bdv
                b, ip = a // (2**combo), ip + 2
            case 7:  # cdv
                c, ip = a // (2**combo), ip + 2
    return output


def search_a(program, a=0, b=0, c=0, pos=-1):
    if abs(pos) > len(program):
        return a
    for i in range(8):
        if run(program, a * 8 + i, b, c)[0] == program[pos]:  # a*8+i matches program output backwards
            e = search_a(program, a * 8 + i, b, c, pos - 1)
            if e:
                return e
    return None


if __name__ == "__main__":
    program = list(map(int, "0,3,5,4,3,0".split(",")))
    print("Part 1:", run(program, a=2024))
    part2 = search_a(program)
    print("Part 2:", part2)
