# Q2 — The Server Room
# A data center has 8 servers. 
# Each server runs some processes. 
# You need to reassign processes across servers to minimize load imbalance. 
# Migrating a process has a cost (downtime in seconds). There is no "goal state" — just keep improving until no reassignment helps. A server is overloaded if its total load exceeds its threshold.

# Task: Find the best process-to-server assignment. Display cost at each improvement step.
import numpy as np
import random

random.seed(42)

CapPerServer = [int(x) for x in np.random.randint(1,6,size=8)]
CurrentProcessesPerServer = [int(x) for x in np.random.randint(1,6,size=8)]

def cost(A,B):
    cost = 0
    for i in range(len(A)):
        if A[i]>B[i]: # over loaded
            cost = cost + 20
        elif A[i]<B[i]-5: #under utilized
            cost = cost + 20
    return cost


def generate_neighbours(allocation):
    neighbours = []
    for i in range(len(allocation)-1):
        for j in range(i+1,len(allocation)):
            nb = []
            for k in range(len(allocation)):
                nb.append(allocation[k])
            temp = nb[i]
            nb[i] = nb[j]
            nb[j] = temp
            neighbours.append(nb)
    return neighbours

#Steepest Ascent
def hillClimb(allocation):

    while True:
        current_allocation = allocation
        current_cost = cost(allocation,CapPerServer)

        temp = current_allocation.copy() # just to be safe for comparison if mutation occurs
        
        for nb in generate_neighbours(current_allocation):
            if cost(nb,CapPerServer) < current_cost:
                current_allocation = nb
                current_cost = cost(nb,CapPerServer)

        if temp != current_allocation:
            allocation = current_allocation
        else:
            print(f"Final allocation is : {[int(x) for x in current_allocation]}")
            print(f"The cost is : {current_cost}")
            break

hillClimb(CurrentProcessesPerServer)