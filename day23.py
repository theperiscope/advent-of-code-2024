# this implementation is faster than the n***3 initial one
def find_triangles(graph):  # triangle is a complete subgraph of 3 nodes, a clique
    triangles, t_count = set(), 0
    # only check neighbors of neighbors to reduce search space
    for first in graph:
        # for each neighbor of the current node
        first_neighbors = graph[first]
        for second in first_neighbors:
            # only check one (the sorted set) direction of trangles to avoid duplicates and speed it up
            if second > first:
                # check common neighbors between node and neighbor
                common_first_second_neighbors = first_neighbors & graph[second]  # interesting: python list intersection
                for third in common_first_second_neighbors:
                    # only count when third node is greater than neighbor
                    # this ensures we count each triangle exactly once
                    if third > second:
                        triangles.add((first, second, third))
                        if any(node.startswith("t") for node in (first, second, third)):
                            t_count += 1

    return len(triangles), t_count


# https://en.wikipedia.org/wiki/Clique_%28graph_theory%29
# a maximum clique of a graph, G, is a clique, such that there is no clique with more vertices.
# Bron-Kerbosch algorithm: https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def find_max_clique(graph):
    def bron_kerbosch(r, p, x, best_clique):
        if len(p) == 0 and len(x) == 0:
            if len(r) > len(best_clique[0]):
                best_clique[0] = r.copy()
            return

        # if we can't possibly beat the best clique, stop
        if len(r) + len(p) <= len(best_clique[0]):
            return

        # choose pivot vertex from p ∪ x that maximizes |p ∩ neighbors(u)|
        pivot_vertex = None
        max_intersection = -1
        for u in p | x:
            intersection_size = len(graph[u] & p)
            if intersection_size > max_intersection:
                max_intersection = intersection_size
                pivot_vertex = u

        # for each vertex not connected to pivot
        for v in p - (graph[pivot_vertex] if pivot_vertex else set()):
            neighbors = graph[v]
            bron_kerbosch(r | {v}, p & neighbors, x & neighbors, best_clique)

            # interesting: https://www.freecodecamp.org/news/python-set-operations-explained-with-examples/
            p = p - {v}  # interesting: set difference operator
            x = x | {v}  # interesting: union operator

    # initialize sets for the algorithm
    vertices, best_clique = set(graph.keys()), [set()]  # use list to allow modification in recursive function

    # start with all vertices in P, none in R or X
    bron_kerbosch(set(), vertices, set(), best_clique)

    return sorted(best_clique[0])


with open("day23.txt", "r") as file:
    connections = file.read().split("\n")

graph = {}
for a, b in (conn.split("-") for conn in connections):
    graph.setdefault(a, set()).add(b)  # interesting: setdefault
    graph.setdefault(b, set()).add(a)

total, t_count = find_triangles(graph)
print("Part 1:", t_count)

max_clique = find_max_clique(graph)
password = ",".join(max_clique)
print("Part 2:", password)
