import random
import math

city = [
  [ 0, 12, 19,  8, 15, 22],
  [12,  0,  9, 14,  6, 18],
  [19,  9,  0, 11, 17,  5],
  [ 8, 14, 11,  0, 20, 13],
  [15,  6, 17, 20,  0, 10],
  [22, 18,  5, 13, 10,  0]
]

def cost(state,grid):
    #duplicates tu koi aye ga hi nahi salay :)
    #cost = 0 # can shadow if the function name is same 
    penalty = 0
    """
    visited = set()
    cost = 0
    state = state + [0]
    for i in range(len(state)):
        if state[i] not in visited:
            visited.add(state[i])
        else:
            continue
        for j in range(len(state)):
            if i!=j :
                if (state[i] == state[j]) and (state[i] != 0 and state[j] != 0):
                    cost = cost + 20
    """
    route = [0] + state + [0]
    for i in range(len(route)-1):
        penalty = penalty + grid[route[i]][route[i+1]]
    return penalty



def generate_neighbours(state):
    neighbours = []
    for i in range(len(state)):
        for j in range(i+1,len(state)):
            nb = []
            for k in range(len(state)):
                nb.append(state[k])
            temp = nb[i]
            nb[i] = nb[j]
            nb[j] = temp
            neighbours.append(nb)
    return neighbours



def SimulatedAnnealing(state, grid):
    T = 1000
    Tmin = 0.1
    alpha = 0.95

    best_state = []
    best_cost = float('inf')

    while T>Tmin:
        current_state = state
        current_cost = cost(state,grid)

        nb = generate_neighbours(state)
        pickState = random.choice(nb)
        pickCost = cost(pickState,grid)

        delta = pickCost - current_cost
        
        if delta<0:
            state = pickState
            current_cost = pickCost
        else:
            P = math.exp(-delta/T)
            if random.random() < P:
                state = pickState
                current_cost = pickCost
        
        if current_cost < best_cost:
            best_cost = current_cost
            best_state = state[:] #copy of state instead of deep copy function
            #ya tu state update ho geyi hodi ya wohi 'current_state' wali value
            # so this is better to use instead of pickState 

          #  best_state = pickState; pick state can cause issues in the very first iteration if pick is rejected and cost of best is inifinity 

        T = T * alpha
    

    print(f"The best state is : {[0] + best_state + [0]}")
    print(f"The cost is {best_cost}")

        
initial = [1,2,3,4,5]
SimulatedAnnealing(initial,city)





































