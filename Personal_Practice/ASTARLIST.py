import heapq
from collections import deque
import math

#heuristic
def manhattan(start, goal):
    sr, sc = start[0], start[1]
    gr, gc = goal[0], goal[1]

    return (abs(gr-sr) + abs(gc-sc))



def ASTAR(start, goal, graph):
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

        for nb, edge_cost in graph[current]:
            if nb not in visisted:
                new_gcost = g_cost + edge_cost
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


graph = {
    (0,0): [((0,1),1), ((1,0),4)],
    (0,1): [((0,0),1), ((0,2),2)],
    (0,2): [((0,1),2), ((1,2),3)],
    (1,0): [((0,0),4), ((2,0),2)],
    (1,2): [((0,2),3), ((2,2),2)],
    (2,0): [((1,0),2), ((2,1),1)],
    (2,1): [((2,0),1), ((2,2),5)],
    (2,2): [((2,1),5), ((1,2),2)]
}

start = (0,0)
goal  = (2,2)

print("Start:", start)
print("Goal :", goal)
print()

ASTAR(start, goal, graph)

