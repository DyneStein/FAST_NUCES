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


def DFS(start, goal, graph):
    parent = {start:None}
    visited = set()

    stack = deque();
    stack.append(start);

    path = []

    while stack:
        current = stack.pop()
        print(current)
        
        if current in visited:
            continue

        visited.add(current);

        if current == goal:   #after the visited check.
            break
        
        for neighbour in graph[current]:
            if neighbour not in visited:
                if neighbour not in parent:
                    parent[neighbour] = current
                    stack.append(neighbour) #made this in the inner if condition

    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    

    path.reverse();
    print(path);




DFS("Central", "Terminal_A",metro_map)












