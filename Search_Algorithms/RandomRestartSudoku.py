
import numpy as np
import random
import copy #for deep copy

def cost(stateOfBoard):
    visited = set()
    cost = 0
    #row wise check
    for i in range(9):
        for j in range(9):
            if stateOfBoard[i][j] not in visited:
                visited.add(stateOfBoard[i][j])
            else:
                cost = cost + 20
        visited.clear()


    #columne wise check
    for i in range(9):
        for j in range(9):
            if stateOfBoard[j][i] not in visited:
                visited.add(stateOfBoard[j][i])
            else:
                cost = cost + 20
        visited.clear()

    #now sub-grid check
    for a in range(3):
        for b in range(3):
            visited.clear()
            for i in range(3):
                for j in range(3):
                    row = a*3 + i #fix
                    col = b*3 + j #fix
                    if stateOfBoard[row][col] not in visited:
                        visited.add(stateOfBoard[row][col])
                    else:
                        cost = cost + 20
            
        
    return cost


#Now, there are two ways to optimise the random restart :
# 1)- Use Stochastic Hill Climbing inside Random Restart
# 2)- Use a better and optimised generate_neighbours function so that we have less more precise neighbours to explore 


def generate_neighbours(state):
    temp = copy.deepcopy(state) #deep copy fix
    neighbours = []
    for i in range(9):
        for j in range(9):
            current_item = state[i][j]
            for a in range(9):
                for b in range(9):
                    state = copy.deepcopy(temp) #deep copy fix
                    if a!=i and b!=j:
                        state[i][j] = state[a][b]
                        state[a][b] = current_item
                        neighbours.append(state)

    return neighbours


"""
def RandomRestart(line):
    temp = line.copy()

    best_cost = float('inf') #initial best cost tuny zero rakhi huii thy salay
    best_state = []

    i = 100
    while i>=0:
        SudokuBoard = []
        for j in range(9):
            random.shuffle(line)
            SudokuBoard.append(line)
            line = temp.copy() #according to GPT there should be a new variable here instead of using line from above

        while True:
            current_cost = cost(SudokuBoard)
            current_board = copy.deepcopy(SudokuBoard)


            for nb in generate_neighbours(SudokuBoard):
                if cost(nb) < current_cost:
                    current_cost = cost(nb)
                    current_board = copy.deepcopy(nb)

            #maintaining the global min
            if current_cost < best_cost:
                best_cost = current_cost
                best_state = copy.deepcopy(current_board)
                print(f"The current best state is : ")
                for k in range(9):
                    print(best_state[k])
                print(f"The current cost is : {best_cost}")
                print()

            if current_cost != cost(SudokuBoard):
                SudokuBoard = copy.deepcopy(current_board)
            else:
                break 
        
        if best_cost == 0:
            break
        i = i-1

    print("="*20)
    print("="*20)
    print(f"The final best state is : ")
    for k in range(9):
        print(best_state[k])
    print(f"The cost is : {best_cost}")
    print("="*20)
    print("="*20)
"""


line = [1,2,3,4,5,6,7,8,9]


def RandomRestart(line):
    temp = copy.deepcopy(line)

    i = 100

    best_state = []
    best_cost = float('inf')


    while i>=0:
        sudoku = []
        for j in range(9):
            random.shuffle(line)
            sudoku.append(line)
            line = copy.deepcopy(temp)

        k = 100
        while k>=0:
            #[I think this implementation is a bit incorrcect]

            #stochastic hill climbing
            nb = generate_neighbours(sudoku)
            nba = random.choice(nb) #random choice

            current_cost = cost(nba)
            current_state = copy.deepcopy(nba)

            if current_cost < best_cost:
                best_state = copy.deepcopy(current_state)
                best_cost = current_cost
                print(f"The current best state is : ")
                for k in range(9):
                    print(best_state[k])
                print(f"The current cost is : {best_cost}")
                print()

            if current_cost < cost(sudoku):
                sudoku = copy.deepcopy(current_state)
            
            k = k-1

        i = i-1

    print(f"The best state is : ")
    for k in range(9):
        print(best_state[k])
    print(f"The best cost is : {best_cost}")
    print()


RandomRestart(line)



    










