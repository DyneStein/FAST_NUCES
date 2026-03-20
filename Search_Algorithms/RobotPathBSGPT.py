import random

grid = [
    [0,0,0,-1,0],
    [-1,0,0,-1,0],
    [-1,-1,0,-1,0],
    [0,-1,0,0,0],
    [0,0,0,-1,0]
]

def cost(state, goal, grid):
    # Manhattan heuristic
    return abs(goal[0]-state[0]) + abs(goal[1]-state[1])


def generate_neighbours(state, grid):
    neighbours = []
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    for dr, dc in directions:
        newRow = state[0] + dr
        newCol = state[1] + dc

        if 0 <= newRow < len(grid) and 0 <= newCol < len(grid[0]):
            if grid[newRow][newCol] != -1:
                neighbours.append((newRow,newCol))

    return neighbours


def beamSearch(grid):

    beamwidth = 3
    start = (0,0)
    goal = (0,4)

    # (state , path)
    beam = [ (start,[start]) ]

    while beam:

        all_neighbours = []

        for state, path in beam:

            for neighbour in generate_neighbours(state,grid):

                # prevent loops
                if neighbour not in path:
                    new_path = path + [neighbour]
                    all_neighbours.append((neighbour,new_path))

        if not all_neighbours:
            print("No path found")
            return

        # sort using heuristic
        all_neighbours.sort(key=lambda x: cost(x[0],goal,grid))

        # keep best k states
        beam = all_neighbours[:beamwidth]

        # goal check
        for state,path in beam:
            if state == goal:
                print("Goal Reached!")
                print("Path:",path)
                print("Steps:",len(path)-1)
                return path


beamSearch(grid)