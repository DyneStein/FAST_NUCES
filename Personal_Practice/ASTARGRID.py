import heapq
from collections import deque
import math


def check_neighbour(current, grid):
    row , col = current[0], current[1]
    check_list = [(-1,0),(+1,0),(0,+1),(0,-1)] #up down right left
    nb = []
    for r,c in check_list:
        if ( row+r>=0 and row+r<len(grid) ) and (col+c >=0 and col+c<len(grid[0])):
            if grid[row+r][col+c]!=-1:
                nb.append((row+r,col+c))
    
    return nb

#heuristic
def manhattan(start, goal):
    sr, sc = start[0], start[1]
    gr, gc = goal[0], goal[1]

    return (abs(gr-sr) + abs(gc-sc))



def ASTAR(start, goal, grid):
    parent = {start:None}
    visisted = set()
    cost = {start:0}
    
    pq = []
    heapq.heappush(pq, (manhattan(start, goal),0,start))

    while pq:
        f_cost, g_cost , current  = heapq.heappop(pq)
        if current in visisted:
            continue
        visisted.add(current)
        if current == goal:
            break

        for nb in check_neighbour(current, grid):
            if nb not in visisted:
                new_gcost = g_cost + grid[nb[0]][nb[1]]
                if new_gcost < cost.get(nb, float('inf')):
                    cost[nb] = new_gcost
                    parent[nb] = current
                    heapq.heappush(pq, (manhattan(nb,goal)+new_gcost, new_gcost, nb))
    
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    print(path)


grid = [
    [1,  2,  1, -1,  3],
    [4, -1,  2, -1,  2],
    [1,  3,  5,  2,  1],
    [-1, 2, -1,  3,  2],
    [2,  1,  2,  4,  1]
]


ASTAR((0,0),(4,4),grid)

