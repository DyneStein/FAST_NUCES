#Q3 — The Locked Vault
#A vault has a 4-digit code. You start at 0000. Each move changes exactly one digit by ±1 (wraps: 9→0, 0→9). Certain combinations are deadlocked (traps — you cannot leave them). The target code is given.
#Task: Find if the target is reachable, and if yes, the minimum number of moves to reach it. Display the path.
import math

target = [2,5,4,5]

initial = [0,0,0,0]

def get_neighbours(state):
    neighbours = []
    for i in range(4):
        nb = []
        for j in range(4):
            nb.append(state[j])
        nb[i] = nb[i] + 1
        #nb[i] = (nb[i] + 1) % 10
        neighbours.append(nb)
    
    for i in range(4):
        nb = []
        for j in range(4):
            nb.append(state[j])
        nb[i] = nb[i] - 1
        #nb[i] = (nb[i] - 1) % 10
        neighbours.append(nb)
    
    return neighbours


def cost(state, goal):
    sum = 0
    for i in range(4):
        sum= sum+abs(state[i]-goal[i])

    return sum


#another good implementation of cost algorithm making sue that the wrapping works and diff
# of 9 and 0 isnt 9 but 1.
#def cost(state, goal):
#    total = 0

#    for i in range(4):
#        diff = abs(state[i] - goal[i])
#        total = total + min(diff , 10-diff)

#    return total


#Steepest Ascent
def hillClimb(initial, target):
    while True:
        current_state = initial
        current_cost = cost(initial,target)
        
        print()
        print(f"The code is : {current_state}")
        print(f"The cost is : {current_cost}")
        print()

        temp = current_state.copy() #you have been forgetting the copy .copy() ITS IMPORTANT!

        #choosing the best neighbour
        for nb in get_neighbours(current_state):
            if cost(nb,target) < current_cost:
                current_cost = cost(nb, target)
                current_state = nb
        
        if temp != current_state:
            initial = current_state #ALSO YOU HAVE BEEN MISSING THIS LATELY
        else:
            print(f"The final code is : {current_state}")
            print(f"The final cost is : {current_cost}")
            break #YOU MISSED THIS NIGGA


            

hillClimb(initial, target)