
import numpy as np
import random
import copy

grid = [
    [0,0,0,-1, 0],
    [-1,0,0,-1, 0],
    [-1,-1,0,-1,0],
    [0,-1,0,0, 0],
    [0,0,0,-1, 0]
]

"""
def cost(state,goal,grid):
    cost = 0
    if grid[state[0]][state[1]]== -1:
        cost = cost + 50
    #you were missing abs here ! !!!! 
    cost = cost + (abs(goal[0]-state[0])+abs(goal[1]-state[1]))
    return cost



def generate_neighbours(state, grid):
    neighbours = []
    nb = [(0,1),(0,-1),(1,0),(-1,0)]
    for i in range(4):
        if state[0]+nb[i][0]>=0 and state[0]+nb[i][0] < len(grid) and state[1]+nb[i][1]>=0 and state[1]+nb[i][1]<len(grid[0]):
            neighbours.append((state[0]+nb[i][0],state[1]+nb[i][1]))

    return neighbours
"""

def cost(state, goal, grid):
    # just Manhattan distance as heuristic
    return abs(goal[0]-state[0]) + abs(goal[1]-state[1])

def generate_neighbours(state, grid):
    neighbours = []
    nb = [(0,1),(0,-1),(1,0),(-1,0)]
    for i in range(4):
        newRow = state[0]+nb[i][0]
        newCol = state[1]+nb[i][1]
        if newRow>=0 and newRow<len(grid) and newCol>=0 and newCol<len(grid[0]):
            if grid[newRow][newCol] != -1:  # skip walls
                neighbours.append((newRow, newCol))
    return neighbours



def beamSearch(grid):
    beamwidth = 3
    goal = (4,4)
    #starting with (0,0)
    #since its grid based , so state(s) and path list
    MainBeam = [ ( (0,0),[(0,0)] ) ] 
    #OR while MainBeam: (both are god but while MainBeam is preferable)
    while True:
        nb = [] #defined it outside par har 3 neighbours ke alag se saary neighbours hongy
        for mainState,path in MainBeam:
            for neighbour in generate_neighbours(mainState,grid):
                if neighbour not in path:
                    nb.append( (neighbour , path + [neighbour] ) )

        Allneighbours = copy.deepcopy(nb)
        Allneighbours.sort(key=lambda x: cost(x[0],goal,grid))

        beamStates = Allneighbours[:beamwidth]

        for state, path in beamStates:
            if state == goal:
                print(f"Goal Reached !")
                print(f"Path : {path}")
                return path

        #this convergence condition should be applied for picking up best of the best stuff without conditions
        # but here we are not looking for the best of the best and this stucks here at point (0,2) if the goal is (0,4) because the
        #the condition of continuation is that the next three best neighbours should be better or from the next three best neighbours \
        # the first best neighbour should be better thant the main beam best neighbour 
        # and if there is no better neighbour than it is stuck

        # also one important tip is that in places you do not want to go 
        # in grid, than do not consider them in generate neighbours becuase those places are not to be 
        # explored in the first place
        
        # both the while True and while Beam are correct but while Beam is preferable

        # below is the convergence condition 
        # convergance condition should only be used in situations 
        # like server load balancing or TSP problems where there is 
        # no single goal, you want to stop at a position where you hit a minimum (local or global) and
        # can not improve further
        
        #SEE LAB TASK 4E 
        #however if there is a goal but you do NOT know it then also you can use convergence condition to find the best possible or optimal goal 

        #However the convergence condition in path finding GRID problems is harmful, it can cuase stopping before 
        #reeaching the goal
        
        # ALSO keep in mind in the convergence condition, we compare BEST vs BEST 
        # You compare the best of the new beam states against the best of the old beam states.

        """
        if cost(beamStates[0][0],(0,4),grid) < cost(MainBeam[0][0],(0,4),grid):
            print(beamStates[0])
            MainBeam = copy.deepcopy(beamStates)
        else:
            break
        """
        MainBeam = copy.deepcopy(beamStates)
            
beamSearch(grid)


    




        
   
    





























































