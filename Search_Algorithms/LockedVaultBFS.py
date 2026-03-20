#Q3 — The Locked Vault
#A vault has a 4-digit code. You start at 0000. Each move changes exactly one digit by ±1 (wraps: 9→0, 0→9). Certain combinations are deadlocked (traps — you cannot leave them). The target code is given.
#Task: Find if the target is reachable, and if yes, the minimum number of moves to reach it. Display the path.
import math
from collections import deque

target = [2,5,4,5]

initial = [0,0,0,0]

def get_neighbours(state):
    neighbours = []
    for i in range(4):
        nb = []
        for j in range(4):
            nb.append(state[j])
        nb[i] = (nb[i] + 1) % 10
        neighbours.append(nb)
    
    for i in range(4):
        nb = []
        for j in range(4):
            nb.append(state[j])
        nb[i] = (nb[i] - 1) % 10
        neighbours.append(nb)
    
    return neighbours


def cost(state, goal):
    sum = 0
    for i in range(4):
        sum= sum+min(abs(state[i]-goal[i]),abs(10-(state[i]-goal[i])))

    return sum


#another good implementation of cost algorithm making sue that the wrapping works and diff
# of 9 and 0 isnt 9 but 1.
#def cost(state, goal):
#    total = 0

#    for i in range(4):
#        diff = abs(state[i] - goal[i])
#        total = total + min(diff , 10-diff)

#    return total


def BFS(init, targ):
    
    #converting initial to string
    initial = ""
    for i in range(len(init)):
        initial = str(initial) + str(init[i])
    
    target = ""
    for i in range(len(targ)):
        target = str(target) + str(targ[i])
    

    parent = {initial:None}
    visited = set()

    queue = deque()
    queue.append(initial)

    visited.add(initial)

    while queue:
        current = queue.popleft()

        if current == target:
            break

        #extremely useful way to convert string to list and even change the data type midway
        for nba in get_neighbours([int(x) for x in current]):
            nb = ""
            for i in range(len(nba)):
                nb = str(nb) + str(nba[i])
            if nb not in visited:
                visited.add(nb)
                parent[nb] = current
                queue.append(nb)
    
    if target not in parent:
        print("Path not found")
    else:
        current = target
        path = []
        while current is not None:
            path.append(current)
            current = parent[current]
        
    path.reverse()
    print(f"The final path is : {path}")
    

BFS(initial,target)



