import random

def Generate_neighbours(state):
    neighbours = []
    for i in range(len(state)):
        for c in 'qwertyuiopasdfghjklzxcvbnm':
            newChar = c
            newword = str(state[:i]) + str(newChar) + str(state[i+1:])
            neighbours.append(newword)
            
    return neighbours



def cost(state,goal):
    penalty = 0
    for i in range(len(state)):
        penalty = penalty + abs( ord(goal[i]) - ord(state[i]) )
    
    return penalty




def beamSearch(start , goal):

    beamWidth = 2

    #vry heavy fix , wese sart it was trating it as a string individually iterable and stuff which is incorrect 
    current_beam = [start]

    while True:
        nb = []
        for part in current_beam:
            for neighbour in Generate_neighbours(part):
                nb.append(neighbour)
        
        nb.sort(key = lambda x : cost(x,goal))

        nb = nb[:beamWidth]

        print()
        print(f"Current best state is : {nb[0]}")
        print(f"Current best cost is : {cost(nb[0],goal)}")
        print()

        if nb[0] == goal:
            print(f"The best state is : {nb[0]}")
            print(f"The best cost is : {cost(nb[0],goal)}")
            print("GOAL REACHED !")

            break

        current_beam = nb


start = "hit"
goal = "cog"
beamSearch(start,goal)












