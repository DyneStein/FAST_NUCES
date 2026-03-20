def cost(state, goal):
    r,c = state[0],state[1]
    gr, gc = goal[0], goal[1]
    return abs(gr-r)+abs(gc-c)

def generate_neighbours(state, grid):
    neighbours = []
    nb = [(0,1),(0,-1),(1,0),(-1,0)]
    for i in range(4):
        if state[0]+nb[i][0] >= 0 and state[0]+nb[i][0] < len(grid) and state[1]+nb[i][1]>=0 and state[1]+nb[i][1]<len(grid[0]):
            if grid[state[0]+nb[i][0]][state[1]+nb[i][1]]!=0:
                neighbours.append((state[0]+nb[i][0],state[1]+nb[i][1]))

    return neighbours

def SimulatedAnnealing(goal, grid):
    T = 1000
    Tmin = 0.1
    alpha = 0.95

    start = ((0,0),[(0,0)])

    best_state = []
    best_cost = float('inf')

    while T>Tmin:
        current_cost = cost(start[0],goal)
        current_state = start[0]
        current_path = start[1]

        nb = generate_neighbours(start[0])
        chosenState = random.choice(nb)
        pickState = (chosenState,current_path.append(chosenState))
        pickCost = cost(pickState[0],goal)

        delta = pickCost - current_cost
        
        if delta < 0:
            start = pickState
            current_cost = pickCost
        else:
            P = math.exp(-delta/T)
            if random.random() < P:
                start = pickState
                current_cost = pickCost

        if current_cost < best_cost:
            best_cost = current_cost
            best_state = start

        T = T*alpha
