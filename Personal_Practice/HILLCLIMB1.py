import numpy as np

CapPerCourse = list(np.random.randint(70,100,size = 12))
ProjectorNeedPerCourse = [True,False,False,True,True,True,False,True,False,True,False,True]

ProjectorPerHall = [False,False,True,True,False,True]
CapPerHall = list(np.random.randint(150,250,size = 6))

allocation = list(np.random.randint(0,6,size = 12))


#Wasbugged -> I was assuming that the capacity of courses allocated to same hall is same
#Now Correct
def cost(allocation, CPH, PPH, CPC, PNC):
    penalty = 0
    visited = set()
    for i in range(len(allocation)):    
        if allocation[i] not in visited:
            visited.add(allocation[i])
        else:
            continue
        capacity = CPH[allocation[i]]
        CurrentCap = CPC[i]
        for j in range(i+1, len(allocation)):
            if allocation[i]==allocation[j]:
                CurrentCap = CurrentCap + CPC[j]
        
        if CurrentCap > capacity : #over used
            penalty = penalty + 45
        elif CurrentCap < capacity: #under used
            penalty = penalty + 45
        


    #projector utilization mismatch
    for i in range(len(allocation)):
        if PNC[i] == True and PPH[allocation[i]] == False:
            penalty = penalty + 20  

    #overall Hall untilization imbalance 
    # i.e over capacity and projector mismatch is done in the previous steps
    # So, I am not adding this final constraint

    return penalty


def generate_neighbour(allocation):
    neighbours = []
    for i in range(len(allocation)):
        for j in range(i+1, len(allocation)):
            nb = [] # I accidently overWrote the np comming from numpy [KEEP AN EYE ON THIS]
            for k in range(len(allocation)):
                nb.append(allocation[k])
            temp = nb[i]
            nb[i] = nb[j]
            nb[j] = temp
            neighbours.append(nb)
    return neighbours


def hillClimbing(allocation):

    while True:
        current_cost = cost(allocation, CapPerHall, ProjectorPerHall,CapPerCourse,ProjectorNeedPerCourse)
        current_allocation = allocation
        temp = current_cost

        nb = generate_neighbour(allocation)


        for i in range(len(nb)):
            if cost(nb[i],CapPerHall, ProjectorPerHall,CapPerCourse,ProjectorNeedPerCourse) < current_cost:
                current_cost = cost(nb[i],CapPerHall, ProjectorPerHall,CapPerCourse,ProjectorNeedPerCourse)
                current_allocation = nb[i]

        if temp != current_cost:
            allocation = current_allocation #move to the next state if improvement fonuds [KEEP AN EYE HERE AS WELL]
        else:
            print("Local Optimum reached. No other neighbour is optimal than current one.")
            #int(x) for x in .... wala kaam is liye kiya hai becuase numpy arrays are differnet from python lists to manually converting to display in simple list form
            print(f"The current optimal allocation is : {[int(x) for x in current_allocation]}")
            print(f"The cost of current allocation is : {current_cost}")
            break


hillClimbing(allocation)