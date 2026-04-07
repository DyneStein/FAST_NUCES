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


def DFS(start, goal, grid):
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
        
        for neighbour in check_neighbour(current,grid):
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



matrix = [
    [0,1,0,0],
    [0,0,1,1],
    [1,0,0,1],
    [0,0,0,0],
]


DFS((0,0),(3,0),matrix)












