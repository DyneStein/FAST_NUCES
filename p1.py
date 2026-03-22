graph = {
    'S': [('A', 2), ('B', 1)],
    'A': [('C', 2), ('G', 9)],
    'B': [('C', 5)],
    'C': [('D', 1)],
    'D': [('G', 3)],
    'G': []
}

start = 'S'
goal = 'G'

#implementing ASTAR for practice
import heapq

'''
def heuristic(start,goal):
    sr,sc = start[0],start[1]
    gr,gc = goal[0], goal[1]

    return (abs(gr-sr) + abs(gc-sc)) 
'''


def ASTAR(start,goal,graph):
    parent = {start:None}
    g_cost = {start:0}
    visited = set()
    

    queue = []
    heapq.heappush(queue, (0,start))

    while queue:
        g,current = heapq.heappop(queue)

        if current in visited:
            continue

        if current==goal:
            break

        visited.add(current)

        for nb,edgeCost in graph[current]:
            new_cost = edgeCost + g
            if nb not in visited:
                if new_cost < g_cost.get(nb,float('inf')):
                    g_cost[nb] = new_cost
                    parent[nb] = current
                    heapq.heappush(queue, (new_cost, nb) )

    if goal not in parent:
        print("Goal not found !")
    
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    print(f"The final path to goal is : {path}")            



ASTAR('S','G',graph)












