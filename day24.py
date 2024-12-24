def evaluate_gate(gate_type, input1, input2):
    gate_operations = {
        "AND": lambda x, y: 1 if (x == 1 and y == 1) else 0,
        "OR": lambda x, y: 1 if (x == 1 or y == 1) else 0,
        "XOR": lambda x, y: 1 if (x != y) else 0,
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
        gate_parts = input_part.split()

        input1, gate_type, input2 = gate_parts
        gates.append((gate_type, input1, input2, output))

    return wires, gates, len(wires) // 2


def part1(wires):
    z_wires = sorted([w for w in wires if w.startswith("z")], key=lambda x: int(x[1:]), reverse=True)
    binary = "".join(str(wires[w]) for w in z_wires)
    return int(binary, 2)


if __name__ == "__main__":
    with open("day24.txt", encoding="utf8") as f:
        wires, gates, bits = parse_input(f.read().strip())

        wires = simulate_circuit(wires, gates)
        print("Part 1:", part1(wires))

        print("Part 2:", "mostly manualy done by visualizing the circuit and evaluating the gates.")
