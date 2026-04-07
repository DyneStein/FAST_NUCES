import heapq
from collections import deque
import math


def check_neighbour(current, grid):
    row , col = current[0], current[1]
    check_list = [(-1,0),(+1,0),(0,+1),(0,-1)] #up down right left
    nb = []
    for r,c in check_list:
        if ( row+r>=0 and row+r<len(grid) ) and (col+c >=0 and col+c<len(grid[0])):
            if grid[row+r][col+c]==0:
                nb.append((row+r,col+c))
    
    return nb


def BFS(start, goal, grid):
    parent = {start:None}
    visited = set()

    queue = deque();
    queue.append(start);
    
    visited.add(start)

    path = []

    while queue:
        current = queue.popleft()
        print(current)

        if current == goal:   #after the visited check.
            break
        
        for neighbour in check_neighbour(current,grid):
            if neighbour not in visited:
                visited.add(neighbour)
                parent[neighbour] = current
                queue.append(neighbour)

    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    

    path.reverse();
    print(path);



matrix = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
]


BFS((0,0),(3,0),matrix)

