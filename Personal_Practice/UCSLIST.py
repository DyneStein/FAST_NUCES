import heapq

def UCS(start, goal, graph):
    parent = {start:None}
    visited = set()
    cost = {start : 0}

    pq = []
    heapq.heappush(pq, (0, start))

    while pq:
        current_cost , current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            break

        for neighbour,edge_cost in graph[current]:
            if neighbour not in visited:
                new_cost = current_cost + edge_cost
                if new_cost<cost.get(neighbour, float('inf')): # if no cost pehly se in dictionary then assign then float('inf')
                       cost[neighbour] = new_cost
                       parent[neighbour] = current
                       heapq.heappush(pq, (new_cost, neighbour))
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    
    path.reverse()
    print(path)


campus_map = {
    "Admin": [("Library", 2), ("Cafeteria", 3)],

    "Library": [("Lab", 4)],
    "Cafeteria": [("Lab", 1)],

    "Lab": [("Hostel", 3)],
    "Hostel": []

}

UCS("Admin", "Hostel",campus_map)


