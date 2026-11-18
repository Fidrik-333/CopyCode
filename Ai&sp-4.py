
import heapq

# Heuristic function: Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Search Algorithm
def a_star_search(graph, start, goal):

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start, [start]))

    visited = set()

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current == goal:
            return path, g

        if current in visited:
            continue

        visited.add(current)

        for neighbor, cost in graph.get(current, []):
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + heuristic(neighbor, goal)

                heapq.heappush(
                    open_set,
                    (new_f, new_g, neighbor, path + [neighbor])
                )

    return None, float('inf')

# Example Graph
graph = {
    (0, 0): [((1, 0), 1), ((0, 1), 1)],
    (1, 0): [((1, 1), 1), ((0, 0), 1)],
    (0, 1): [((0, 0), 1), ((1, 1), 1)],
    (1, 1): [((1, 0), 1), ((0, 1), 1), ((2, 1), 1)],
    (2, 1): [((1, 1), 1), ((2, 2), 1)],
    (2, 2): [((2, 1), 1)]
}

start_node = (0, 0)
goal_node = (2, 2)

path, cost = a_star_search(graph, start_node, goal_node)

print("A* Search Algorithm")
print("-------------------")
print(f"Start node: {start_node}")
print(f"Goal node: {goal_node}")

if path:
    print(f"Path found: {path}")
    print(f"Total cost: {cost}")
else:
    print("No path found.")
