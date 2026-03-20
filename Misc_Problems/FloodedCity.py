#Q1 — The Flooded City

#A rescue team is navigating a partially flooded city.
#Roads between districts have water levels (cost to traverse). 
#The team starts at the emergency base and must reach a trapped survivor. However, some roads are completely blocked (impassable). The team wants to reach the survivor using the least total water exposure. They also have a rough straight-line distance estimate to the survivor from any district.

#Task: Find the optimal path. Display the path and total cost.

import heapq
from collections import deque
import math


def euclidean(start,goal):
    return math.sqrt(((goal[0]-start[0])**2) + ((goal[1]-start[1])**2) )

def check_neighbours(current, grid):
    nb = [(0,1),(0,-1),(1,0),(-1,0)]
    neighbours = []
    for i in range(4):
        if current[0]+nb[i][0] >= 0 and current[0]+nb[i][0] < len(grid) and current[1]+nb[i][1]>=0 and current[1]+nb[i][1]<len(grid[0]):
            if grid[current[0]+nb[i][0]][current[1]+nb[i][1]] != -1:
                neighbours.append((current[0]+nb[i][0],current[1]+nb[i][1]))
    return neighbours



def ASTAR(start,goal,grid):
    parent = {start : None}
    visited = set()
    g_cost = {start: 0}

    pq = []
    heapq.heappush(pq,(euclidean(start,goal),0,start))
    while pq:
        f , g , current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for nb in check_neighbours(current,grid):
            if nb not in visited:
                new_cost = g + grid[nb[0]][nb[1]]
                if new_cost < g_cost.get(nb, float('inf')):
                    g_cost[nb] = new_cost
                    parent[nb] = current
                    heapq.heappush(pq,(euclidean(nb,goal)+new_cost,new_cost,nb))
    
    if goal not in parent:
        print("Path not found")
        return 0
    else:
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]      
        path.reverse()
        print(path)












grid = [
[1,2,-1,4,5],
[5,4,3,-1,0],
[2,2,-1,0,2],
[0,0,1,1,2],
[-1,-1,-1,1,1]
]


ASTAR((0,0),(0,4),grid)










