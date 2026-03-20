import numpy as np
import random


ServerCapacity = np.random.randint(1,5,size=(6))
print(f"The server capacities are as follow : {[int(x) for x in ServerCapacity]}")

TasksPerServer = np.random.randint(0,6,size = (18))

def cost(state, SC):
    visited = set()
    NumberOfTasks = 0
    cost = 0
    for i in range(len(state)):
        
        if state[i] not in visited:
            visited.add(state[i])
            NumberOfTasks = 1 # resetting here for every different server
        else:
            continue
        for j in range(i+1, len(state)):
            if state[i]==state[j]:
                NumberOfTasks = NumberOfTasks+1
        if NumberOfTasks > SC[state[i]]:
            cost = cost + 20

    return cost        




def generate_neighbours(state):
    neighbours = []
    for i in range(len(state)):
        for j in range(len(state)):
            nb = []
            for k in range(len(state)):
                nb.append(state[k])
            temp = nb[i]
            nb[i] = nb[j]
            nb[j] = temp
            neighbours.append(nb)

    return neighbours



def StochasticHillClimbing(state,SC):
    i = 100
    #iteration wise because stochastic does not stops conventionally
    #becuase we keep on randomly generate states if the currently randomly generated state
    #is not better than the current state
    
    best_state = state
    best_cost = cost(state,SC)


    while i>=0:
        current_state = state
        current_cost = cost(state,SC)

        nb = generate_neighbours(current_state)
        random_state = random.choice(nb)
        
        if cost(random_state,SC)<current_cost:
            state = random_state
        
        if cost(random_state,SC) < best_cost:
            best_cost = cost(random_state,SC)
            best_state = random_state
        
        i = i - 1
    

    print(f"The best state is : {[int(x) for x in best_state]}")
    print(f"The best cost is : {best_cost}")


StochasticHillClimbing(TasksPerServer,ServerCapacity)

        































