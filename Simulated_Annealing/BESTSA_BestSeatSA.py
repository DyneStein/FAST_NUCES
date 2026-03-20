# ⬜ -> not allowed
# 💺 -> empty seats
seats = [
    ["⬜", "⬜", "💺", "💺", "💺", "⬜", "⬜"],
    ["⬜", "💺", "💺", "💺", "💺", "💺", "⬜"],
    ["💺", "💺", "💺", "💺", "💺", "💺", "💺"],
    ["💺", "💺", "💺", "💺", "💺", "💺", "💺"],
    ["💺", "💺", "💺", "💺", "💺", "💺", "💺"]
]


import numpy as np
import random
import copy
import math

def cost(state,grid):
    penalty = 0
    penalty = state[0] + state[1]
    nb = [(0,1),(0,-1),(1,0),(-1,0)]
    for i in range(4):
        if (state[0]+nb[i][0])>=0 and (state[0]+nb[i][0])<len(grid) and (state[1]+nb[i][1])>=0 and (state[1]+nb[i][1])<len(grid[0]):
            if grid[state[0]+nb[i][0]][state[1]+nb[i][1]] == "⬜":
                penalty = penalty + 10
    
    return  penalty



def generate_neighbours(state,grid):
    neighbours = []
    nb = [(0,1),(0,-1),(1,0),(-1,0)]
    for i in range(4):
        if (state[0]+nb[i][0])>=0 and (state[0]+nb[i][0])<len(grid) and (state[1]+nb[i][1])>=0 and (state[1]+nb[i][1])<len(grid[0]):
            if grid[state[0]+nb[i][0]][state[1]+nb[i][1]] == "💺":
                neighbours.append( (state[0]+nb[i][0],state[1]+nb[i][1]) )

    return neighbours



def simulatedAnnealing(state,grid):
    T = 1000
    Tmin = 0.1
    alpha = 0.95

    #fix
    current_state = state

    best_state = current_state
    best_cost = cost(current_state,grid)
    
    while T>Tmin:
        
        #fix
        current_cost = cost(current_state,grid)

        
        nb = generate_neighbours(current_state,grid)
        
        if not nb:
            break
        
        pickState = random.choice(nb)
        pickCost = cost(pickState,grid)


        delta = pickCost - current_cost

        if delta<0:
            current_state = pickState
        else:
            P = math.exp(-delta/T)
            if random.random() < P:
                current_state = pickState

        current_cost = cost(current_state,grid)

        if current_cost < best_cost:
            best_cost = current_cost
            best_state = current_state
            print(f"The current best seat is : {best_state}")
            print(f"The current best cost is : {best_cost}")

        T = T*alpha

    print(f"The best seat is : {best_state}")
    print(f"The best cost is : {best_cost}")



simulatedAnnealing((4,6),seats)