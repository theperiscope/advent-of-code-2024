def evaluate_gate(gate_type, input1, input2):
    gate_operations = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "XOR": lambda x, y: x ^ y,
    }
    return gate_operations[gate_type](input1, input2)


def simulate_circuit(wires, gates):
    while True:
        made_progress = False
        for op, a, b, output in gates:
            if output not in wires and a in wires and b in wires:
                wires[output] = evaluate_gate(op, wires[a], wires[b])
                made_progress = True
        if not made_progress:
            break
    return wires


def parse_input(text):
    wires, gates, sections = {}, [], text.strip().split("\n\n")

    for line in sections[0].split("\n"):
        wire, value = map(str.strip, line.split(":"))
        wires[wire] = int(value)

    for line in sections[1].split("\n"):
        input_part, output = map(str.strip, line.split("->"))
        input1, gate_type, input2 = input_part.split()
        gates.append((gate_type, input1, input2, output))

    return wires, gates, len(wires) // 2


def part1(wires):
    z_wires = sorted([w for w in wires if w.startswith("z")], key=lambda x: int(x[1:]), reverse=True)
    binary = "".join(str(wires[w]) for w in z_wires)
    return int(binary, 2)


# inspired by well-documented code from https://github.com/xhyrom/aoc/blob/main/2024/24/part_2.py
def find_output_wire(left, right, operation, gates):
    for op, a, b, output in gates:
        if {a, b} == {left, right} and op == operation:  # interesting: set comparison for unordered equality
            return output
    return None


# interesting: Full Adders in Digital Logic
def full_adder_logic(x, y, c0, gates, swapped):
    """
    Full Adder Logic:
    A full adder adds three one-bit numbers (X1, Y1, and carry-in C0) and outputs a sum bit (Z1) and a carry-out bit (C1).
    The logic for a full adder is as follows:
    - X1 XOR Y1 -> M1 (intermediate sum)
    - X1 AND Y1 -> N1 (intermediate carry)
    - C0 AND M1 -> R1 (carry for intermediate sum)
    - C0 XOR M1 -> Z1 (final sum)
    - R1 OR N1 -> C1 (final carry)

    Args:
    - x: input wire x
    - y: input wire y
    - c0: input carry
    - gates: list of gates
    - swapped: list of swapped wires

    Returns:
    - z1: final sum
    - c1: final carry

    References:
    - https://www.geeksforgeeks.org/full-adder/
    - https://www.geeksforgeeks.org/carry-look-ahead-adder/
    - https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder
    """

    m1 = find_output_wire(x, y, "XOR", gates)  # X1 XOR Y1 -> M1 (intermediate sum)
    n1 = find_output_wire(x, y, "AND", gates)  # X1 AND Y1 -> N1 (intermediate carry)

    if c0 is not None:
        r1 = find_output_wire(c0, m1, "AND", gates)  # C0 AND M1 -> R1 (carry for intermediate sum)
        if not r1:
            n1, m1 = m1, n1
            swapped.extend([m1, n1])
            r1 = find_output_wire(c0, m1, "AND", gates)

        z1 = find_output_wire(c0, m1, "XOR", gates)  # C0 XOR M1 -> Z1 (final sum)

        if m1 and m1.startswith("z"):
            m1, z1 = z1, m1
            swapped.extend([m1, z1])

        if n1 and n1.startswith("z"):
            n1, z1 = z1, n1
            swapped.extend([n1, z1])

        if r1 and r1.startswith("z"):
            r1, z1 = z1, r1
            swapped.extend([r1, z1])

        c1 = find_output_wire(r1, n1, "OR", gates)  # R1 OR N1 -> C1 (final carry)
    else:
        z1 = m1
        c1 = n1

    return z1, c1


def part2(gates, wires):
    c0 = None
    swapped = []

    bits = len([wire for wire in wires if wire.startswith("x")])
    for i in range(bits):
        x, y = f"x{i:02}", f"y{i:02}"
        z1, c1 = full_adder_logic(x, y, c0, gates, swapped)

        if c1 and c1.startswith("z") and c1 != "z45":
            c1, z1 = z1, c1
            swapped.append(c1)
            swapped.append(z1)

        # update carry
        c0 = c1 if c1 else find_output_wire(x, y, "AND", gates)

    return ",".join(sorted(swapped))


if __name__ == "__main__":
    with open("day24.txt", encoding="utf8") as f:
        wires, gates, bits = parse_input(f.read().strip())

        wires = simulate_circuit(wires, gates)
        print("Part 1:", part1(wires))

        print("Part 2:", part2(gates, wires))
