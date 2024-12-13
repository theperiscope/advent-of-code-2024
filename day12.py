class Box:
    def __init__(self, box_type, coordinates):
        self.box_type = box_type
        self.coordinates = coordinates
        self.area = len(coordinates)
        self.perimeter = self.calculate_perimeter()
        self.side_count = self.get_side_count()

    def calculate_perimeter(self):
        perimeter = 0
        for x, y in self.coordinates:
            if (x - 1, y) not in self.coordinates:
                perimeter += 1
            if (x + 1, y) not in self.coordinates:
                perimeter += 1
            if (x, y - 1) not in self.coordinates:
                perimeter += 1
            if (x, y + 1) not in self.coordinates:
                perimeter += 1
        return perimeter

    def get_side_count(self):
        side_count = 0
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in offsets:
            analyzed = set()
            for x, y in self.coordinates:
                if (x, y) in analyzed:
                    continue
                if (x + dx, y + dy) in self.coordinates:
                    continue
                side_count += 1
                for scan_delta in (-1, 1):
                    r, c = x, y
                    while (r, c) in self.coordinates and (r + dx, c + dy) not in self.coordinates:
                        analyzed.add((r, c))
                        # Scan perpendicular to the offset direction
                        r += -dy * scan_delta  # Switch dy and dx to scan perpendicular
                        c += -dx * scan_delta
        return side_count


def parse_floor(floor):
    def get_neighbors(x, y):
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if x < len(floor[0]) - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < len(floor) - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def bfs(start, box_type):
        queue = [start]
        visited = set()
        visited.add(start)
        coordinates = []
        while queue:
            x, y = queue.pop(0)
            coordinates.append((x, y))
            for nx, ny in get_neighbors(x, y):
                if (nx, ny) not in visited and floor[ny][nx] == box_type:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return coordinates

    boxes = []
    visited = set()
    for y, row in enumerate(floor):
        for x, box_type in enumerate(row):
            if (x, y) not in visited:
                coordinates = bfs((x, y), box_type)
                visited.update(coordinates)
                boxes.append(Box(box_type, coordinates))
    return boxes


with open("day12.txt", encoding="UTF-8") as f:
    floor = [line.strip() for line in f]

boxes = parse_floor(floor)

print("Part 1:", sum(box.area * box.perimeter for box in boxes))
print("Part 2:", sum(box.area * box.side_count for box in boxes))
