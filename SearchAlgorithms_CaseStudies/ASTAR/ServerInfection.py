
"""
A company has N servers connected in a network. Each server is identified by an integer ID from 0 to N-1. The network is represented as an undirected weighted graph where edge weights represent latency in milliseconds.

At time T=0, a set of servers infected[] are already compromised by a virus. Every second, the virus spreads from an infected server to an adjacent server — but it always spreads through the lowest-latency connection first. A server gets infected at the moment the virus arrives, and immediately begins spreading further.

You are a network admin. You can sever exactly one edge per second, but only before the virus would travel across it that second. You want to minimize the total number of infected servers at the end.
"""




import heapq

N = 7
edge = [
  (0,1,2), (0,2,5), (1,3,1), (1,4,4),
  (2,4,3), (3,5,2), (4,5,6), (5,6,1)
]


edges = {
    0:[(1,2),(2,5)],
    1:[(3,1),(4,4)],
    2:[(4,3)],
    3:[(5,2)],
    4:[(5,6)],
    5:[(6,1)]
}



# format: (server_a, server_b, latency)


def UCS(start, goal, graph):
    parent = {start : None}
    g_cost = {start:0}
    visited = set()

    queue = []
    heapq.heappush(queue, (0,start))


    while queue:
        cost , current  = heapq.heappop(queue)
        
        if current in visited:
            continue

        if current == goal:
            break

        visited.add(current)

        for nb , edge_cost in graph[current]:
            new_cost = cost + edge_cost
            if new_cost < g_cost.get(nb, float('inf')):
                g_cost[nb] = new_cost
                parent[nb] = current
                heapq.heappush(queue,(new_cost,nb))
    
    if goal not in parent:
        print("No goal found")

    path = []
    current = goal 
    while current is not None:
        path.append(current)
        current = parent[current]
    
    path.reverse()

    print("The final path is : ")
    print(path)



UCS(0,5,edges)

