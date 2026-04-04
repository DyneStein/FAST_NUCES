import random

city = [[random.choice(list(range(1,20))) for i in range(5)] for j in range(5)]

for i in range(5):
    for j in range(5):
        if i==j :
            city[i][j] = 0

print("Current city grid\n")
for i in range(5):
    print(city[i])



def initial_population_generator(pop_size):
    pop = []
    cities = list(range(1,5))
    print("dakjnsjnds") #total cities - 2 ... so for example we have total 5 cities and tum ne kisi aik se start lena starting city + remainging ciies = lets say 5(inclusive of starting), now you also have to get to that starting right! so add one , 5+1 = 6 cities total including starting and ending which is basically the same city so subtract them both so total 6 - 2 = 4 is basically the amount of cities other than the starting / ending one you have to have and make a list and generate populations....
    print(cities)
    print("")
    temp = cities[:]
    for i in range(pop_size):
        #majorFix1
        #RANDOM SHUFFLE INPLACE MODIFY KRTA HAI SALAYYYY IS BAAT KO YAAD RAKH 
        random.shuffle(cities)
        pop.append(cities)
        cities = temp[:]

    return pop



#generally kisi ne agr likha hua hai in exam that C5,C4,C2,C1,C6,C3 is ka matlab implicit hai ke this complete list includes the starting city which is C5 but NOT THE ENDING CITY which is also C5 but not included so in cost calculation keep this thing in mind... 


def cost(chromosome,grid):
    penalty = 0
    chroma = [0] + list(chromosome) + [0]
    for i in range(len(chroma)-1):
        penalty = penalty + grid[chroma[i]][chroma[i+1]]
    
    return penalty



def fitness(chromosome,grid):
    return 1/(1+cost(chromosome,grid))


def touramentSelection(population, tournamentSize, grid):
    
    indices = random.sample(range(len(population)), tournamentSize)

    WinnerIndex = max(indices, key = lambda k : fitness(population[k],grid))

    return population[WinnerIndex]



def OrderCrossOver(parentA, parentB):

    size = len(parentA)

    cut1 = random.randint(0, size-2)
    cut2 = random.randint(cut1+1,size-1)

    child = [None]*size

    for i in range(cut1, cut2+1):
        child[i] = parentA[i]

    used = set()
    for i in range(len(child)):
        if child[i] is not None:
            used.add(child[i])
    

    b_index = cut2+1
    childIndex = 0
    while None in child:
        if b_index==size:
            b_index = 0

        if parentB[b_index] not in used:
            
            while child[childIndex] is not None:
                childIndex = childIndex + 1

            child[childIndex] = parentB[b_index]
        #fix2
        #ye index tu har outer iteration ke saaath update hona chahiye chahe child update hua ya nahi
        b_index = b_index + 1
    
    return child


def getElites(population, elitesSize,grid):

    fitnesses = [fitness(chromosome,grid) for chromosome in population]
    paired = list(zip(fitnesses,population))
    paired.sort(reverse = True)
    elite = [chromosome for f, chromosome in paired[:elitesSize]]
    return elite



def mutationSwap(child,mutationRate):
    i , j = random.sample(range(len(child)),2)

    r = random.random()

    if r < mutationRate:
        child[i], child[j] = child[j], child[i]
    
    return child



def GeneticAlgo(generationSize, populationSize, mutationRate, grid):
    
    population = initial_population_generator(populationSize)
    best_chromosome = []
    best_cost = -(float('inf'))

    for i in range(generationSize):

        new_population = getElites(population, 5, grid)


        while len(new_population) < populationSize:

            parentA = touramentSelection(population,3,grid)
            parentB = touramentSelection(population,3,grid)
        
            child = OrderCrossOver(parentA, parentB)

            child = mutationSwap(child,mutationRate)

            new_population.append(child)

        population = new_population

        current_best_chromosome = getElites(new_population,1,grid)[0]
        current_best_cost = fitness(current_best_chromosome,grid)

        print(f"Generation {i} best fitness: {current_best_cost}")

        if current_best_cost > best_cost:
            print(f"Current best chromosome is : {[0] + current_best_chromosome + [0]}")
            print(f"Current best cost is : {current_best_cost}")
            best_cost = current_best_cost
            best_chromosome = current_best_chromosome

        
    print(f"The best chromosome is : {[0] + best_chromosome + [0]}")
    print(f"The best cost is : {best_cost}")



GeneticAlgo(50,50,0.1,city)










