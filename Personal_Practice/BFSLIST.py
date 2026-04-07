import heapq
from collections import deque
import math


metro_map = {
    "Central":    ["Line_A1", "Line_B1"],
    "Line_A1":    ["Line_A2"],
    "Line_A2":    ["Line_A3", "Line_A4"],
    "Line_A3":    ["Terminal_A"],
    "Line_A4":    [],
    "Line_B1":    ["Line_B2"],
    "Line_B2":    ["Line_B3"],
    "Line_B3":    ["Terminal_B"],
    "Terminal_A": [],
    "Terminal_B": []
}

def BFS(start, goal , graph):
    parent = {start:None}
    visited = set()

    queue = deque()
    queue.append(start)

    visited.add(start)

    while queue:
        current = queue.popleft()
        print(current)
        
        if current == goal:
            break

        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                parent[neighbour] = current
                queue.append(neighbour)
    
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent.get(current)
    
    path.reverse()
    print(path)


BFS("Central", "Terminal_B", metro_map)










