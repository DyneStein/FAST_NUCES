graph = {
    'S': [('A', 2), ('B', 1)],
    'A': [('C', 2), ('G', 9)],
    'B': [('C', 5)],
    'C': [('D', 1)],
    'D': [('G', 3)],
    'G': []
}

start = 'S'
goal = 'G'


#implementing ASTAR for practice
from 

def heuristic(start,goal):
    sr,sc = start[0],start[1]
    gr,gc = goal[0], goal[1]

    return (abs(gr-sr) + abs(gc-sc)) 


def UCS(start,goal,graph):
    parent = {start:None}
    g_cost = {start:None}
    h_cost = {start:0}
    visited = set()

    queue = []
    


















