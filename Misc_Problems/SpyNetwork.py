
import heapq


#Q5 — The Spy Network
#A spy must pass a secret message through a network of agents. Each agent connection has a risk score. The spy starts at Agent 0 and must reach Agent N. Some agents are compromised — passing through them doubles the risk of all subsequent edges. The spy wants the lowest total risk path, and has a heuristic estimate of remaining risk from any agent.
#Task: Find the safest path. Display each node visited and cumulative risk.


def heuristic(start, goal):
    sr , sc = start[0], start[1]
    gr, gc = goal[0], goal[1]

    return abs(gr-sr) + abs(gc-sc)


def generate_neighbours(state,grid):
    nb = [(-1,0),(1,0),(0,-1),(0,1)]
    fn = []
    for i in range(4):
        if state[0]+nb[i][0]>=0 and state[0]+nb[i][0]<len(grid) and state[1]+nb[i][1]>=0 and state[1]+nb[i][1]<len(grid[0]):
            if grid[state[0]+nb[i][0]][state[1]+nb[i][1]] < 9: #7 is my threshold, above 7 woul be the agents who are compromised
                fn.append((state[0]+nb[i][0], state[1]+nb[i][1]))

    return fn


def ASTAR(start, goal, grid):
    parent = {start:None}
    visited = set()
    g_cost = {start:0}

    pq = []
    heapq.heappush(pq, (heuristic(start, goal),0,start))

    while pq:
        f, g , current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for nb in generate_neighbours(current, grid):
            if nb not in visited:
                new_cost = g + grid[nb[0]][nb[1]]
                if new_cost < g_cost.get(nb, float('inf')):
                    g_cost[nb] = new_cost
                    parent[nb] = current
                    heapq.heappush(pq, (heuristic(nb,goal)+new_cost,new_cost,nb))
    
    if goal not in parent:
        print("GOAL NOT REACHED !")
    else:
        current = goal
        path = []
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        print(f"The final path is : {path}")






SpyNetwork = [

[0, 8, 1, 10, 6],
[7, 2, 9, 4, 5],
[6, 10, 3, 1, 8],
[5, 7, 2, 9, 4],
[8, 1, 6, 3, 5]

]


ASTAR((0,0),(4,4),SpyNetwork)

