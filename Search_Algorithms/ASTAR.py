
from collections import deque
import heapq

def heuristic(point, goal):
    sr,sc = point[0],point[1]
    gr,gc = goal[0],goal[1]

    return abs(gr-sr) + abs(gc-sc)




def check_neighbour(point, grid):
    locations = [(0,-1),(0,+1),(1,0),(-1,0)]
    nb = []
    cr,cc = point[0], point[1]
    for i in range(4):
        if cr+locations[i][0] >=0 and cr+locations[i][0]<len(grid) and cc+locations[i][1]>=0 and cc+locations[i][1]<len(grid[0]): 
            if grid[cr+locations[i][0]][cc+locations[i][1]] != -1:
                nb.append((cr+locations[i][0],cc+locations[i][1]))

    return nb



def ASTAR(start,goal,grid):
    parent  = {start:None}
    visited = set()
    g_cost = {start:0}
    
    pq = []
    heapq.heappush(pq, (heuristic(start,goal)+0, 0, start))

    while pq:
        f,g,current = heapq.heappop(pq);

        if current == goal:
            break
        
        if current in visited:
            continue
        visited.add(current)



        for nb in check_neighbour(current, grid):
            if nb not in visited:
                new_cost = g + grid[nb[0]][nb[1]]
                if new_cost<g_cost.get(nb, float('inf')):    
                    g_cost[nb] = new_cost
                    parent[nb] = current
                    heapq.heappush(pq,(heuristic(nb,goal)+new_cost,new_cost,nb))

    if goal not in parent:
        print("Path not found")
        return

    finalPath = []
    current = goal
    while current is not None:
        finalPath.append(current)
        current = parent[current]
    
    finalPath.reverse()

    print(finalPath)




grid = [
[0,-1,2,3,5],
[5,5,-1,5,5],
[-1,6,4,3,9]
]



ASTAR((0,0),(0,4),grid)












