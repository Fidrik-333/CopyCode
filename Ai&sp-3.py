
from collections import deque

# Depth-First Search (DFS)
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)
    print(start, end='')

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

# Breadth-First Search (BFS)
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        print(vertex, end='')

        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# Example graph represented as adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

print("Depth-First Search starting from node A:")
dfs(graph, 'A')

print("\nBreadth-First Search starting from node A:")
bfs(graph, 'A')
