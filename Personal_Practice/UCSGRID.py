import heapq
from collections import deque
import math


def check_neighbour(current, grid):
    row , col = current[0], current[1]
    check_list = [(-1,0),(+1,0),(0,+1),(0,-1)] #up down right left
    nb = []
    for r,c in check_list:
        if ( row+r>=0 and row+r<len(grid) ) and ( col+c >=0 and col+c<len(grid[0]) ):
            if grid[row+r][col+c]!=-1:
                nb.append((row+r,col+c))
    
    return nb



def UCS(start, goal, grid):
    parent = {start:None}
    visited = set()
    cost = {start:0}

    row, col = start[0], start[1]

    path = []

    pq = []
    heapq.heappush(pq,(0 , start)) # adding the tuple with the local cummulative cost
 
    while pq:
        current_cost, current = heapq.heappop(pq)

        if current in visited:
            continue
        
        visited.add(current)
        
        if current==goal:
            break

        for nb in check_neighbour(current, grid):
            if nb not in visited:
                new_cost = current_cost + grid[nb[0]][nb[1]]
                if new_cost<cost.get(nb, float('inf')):
                    cost[nb] = new_cost
                    parent[nb] = current
                    heapq.heappush(pq, (new_cost, nb))
    
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    

    path.reverse()
    print(path)



grid1 = [
    [1, 2, -1, 3, 1],
    [2, -1, 2, 5, 2],
    [1, 3, -1, 4, 2],
    [2, -1, 2, 3, 1],
    [1, 5, 2, -1, 2]
]

print("Grid (1=wall, numbers=cost):")
for row in grid1:
    print(row)
print("\nStart: (0,1)")
print("Goal: (4,4)")
print()

UCS((0,1), (4,4), grid1)
