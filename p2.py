import random
from collections import deque
import heapq

graph = {
    'S': ['A', 'B'],
    'A': ['C'],
    'B': ['D'],
    'C': ['E'],
    'D': ['G'],
    'E': [],
    'G': []
}

values = {
    'S': 10,
    'A': 12,
    'B': 11,
    'C': 11,
    'D': 13,
    'E': 10,
    'G': 14
}

start = 'S'

'''
#implementing first choice and steepest ascent one by one
#here the graph is basically the neighbour generation function
#values is the cost function type shittt

def firstChoice(start,goal_state,graph):
    #it is basically same as the normal/conventional hill climb, we do not use iterative loops yet convergence condition

    best_cost = -float('inf')
    best_state = start

    pick_cost = best_cost
    pick_state = best_state
    
    while True:
        
        current_cost = pick_cost
        current_state = pick_state     
        
        if current_state == goal_state:
            print("GOAL REACHED!")


        for nb in graph[current_state]:
            if values[nb] > pick_cost:
                pick_state = nb
                pick_cost = values[nb]
                break #this is the best first condition
        
        if pick_cost != current_cost:
            current_cost = pick_cost
            current_state = pick_state
        else:
            print("No better neighbour found.")
            break

        if current_cost > best_cost:
            print(f"Current best state is : {current_state}")
            print(f"Current best cost is : {current_cost}")
            best_cost = current_cost
            best_state = current_state


firstChoice('S','G',graph)
#now since the first best isnt deciding/checking all the neighbours , so it is more likely to get stuck in local optimum (max or min)

'''


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



'''
def SteepestAscent(start,goal,graph):
    
    best_state = start
    best_cost = -float('inf')

    pick_cost = best_cost
    pick_state = start

    while True:
        current_cost = pick_cost
        current_state = pick_state

        if current_state == goal:
            print("Goal found.")
            break


        #picking the best neighbour
        for nb in graph[current_state]:
            if values[nb] > pick_cost:
                pick_cost = values[nb]
                pick_state = nb
            
        if pick_cost != current_cost:
            current_cost = pick_cost
            current_state = pick_state
        else:
            print("No good neighbour is found !")
            break
        

        if current_cost > best_cost:
            print(f"Current best state is : {current_state}")
            print(f"Current best cost is : {current_cost}")
            best_cost = current_cost
            best_state = current_state


SteepestAscent('S','G',graph)
#also stuck in the local optimum
'''































