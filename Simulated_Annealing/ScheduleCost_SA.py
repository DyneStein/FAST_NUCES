import numpy as np
import random
import copy
import math

#index position represents the job number 
JobPreference =[int(x) for x in np.random.randint(0 , 5 , size = 5)]
print(f"The current Job preferences are : {JobPreference}")


def cost(state, JP):
    cost = 0
    for i in range(5):
        cost = cost + abs(state[i] - JP[i])
    if abs(state[1]-state[3]) == 1:
        cost = cost +  5
    if abs(state[0]-state[2])==1:
        cost = cost + 5
    
    return cost




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




def SimulatedAnnealing(state, JP):
    T = 1000
    Tmin = 1.5
    alpha = 0.95 # multiplicative factor

    best_cost = cost(state,JP)
    best_state = []

    while T>Tmin:

        current_cost = cost(state, JP)
        current_state = copy.deepcopy(state)
        
        neighbours = generate_neighbours(state)
        pickState =  random.choice(neighbours)
        pickCost = cost(pickState, JP)

        delta = pickCost - current_cost


        if delta<0:
            state = pickState
        else:
            P = math.exp(-delta/T) #- ka sign for the worse case of minimization
            if random.random() < P: #idk why we do this ? 
                state = pickState
                current_cost = pickCost
        
        if current_cost < best_cost:
            best_cost = current_cost # not pick  because we do not know if pick was accepted or not but we do know that current state is accepted
            best_state = current_state
            current_cost = pickCost #current cost kyun ke ab update ho gayi hai tu ab us se compare krna hai 

        T = T*alpha


    print(f"The best state is : { [int(x) for x in best_state] }")
    print(f"The best cost is : {best_cost}")




current = [0,1,2,3,4]
SimulatedAnnealing(current,JobPreference)











