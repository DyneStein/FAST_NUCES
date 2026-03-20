import random

weights = [15,3,8,3]
MAXWEIGHT = 10

def generate_initial_population(pop_size):
    knapsack_size = 4
    nb = []
    for i in range(pop_size):
        bin = [random.choice([0,1]) for i in range(knapsack_size)]
        nb.append(bin)
    
    return nb



def fitness(chromosome):
    cost = 0
    for i in range(len(chromosome)):
        if chromosome[i]==1:
            cost = cost + weights[i]

    
    if cost>MAXWEIGHT:
        cost = cost - 4*( abs(cost-MAXWEIGHT) )

    return cost




def RouletteWheelSelection(population):
    fitnesses = [fitness(chromosome) for chromosome in population]

    totalFitness = sum(fitnesses)

    r = random.random()

    cummulative = 0
    for i in range(len(population)):
        cummulative = cummulative + (fitnesses[i]/(1+totalFitness))
        if r < cummulative:
            return population[i]
    
    return population[-1]



def singlePointCrossOver(parentA, parentB):
    size = len(parentA)

    cut = random.randint(1,size-1)

    child = [None]*size

    for i in range(0,cut):
        child[i] = parentA[i]

    for i in range(cut,size):
        child[i] = parentB[i]

    return child


def bitFlipMutation(child,mutationRate):
    for i in range(len(child)):
        if random.random() < mutationRate:
            child[i] = 1-child[i]

    return child



def elitism(population,eliteSize):

    fitnesses = [fitness(chromosome) for chromosome in population]
    paired = list(zip(fitnesses, population))
    paired.sort(reverse=True) #max in the start
    elite = [chromosome for f,chromosome in paired[:eliteSize]]
    return elite



def GeneticAlgo(generationSize, populationSize,mutationRate):
        population = generate_initial_population(populationSize)
        
        best_chromosome = []
        best_cost = -(float('inf'))

        for i in range(generationSize):

            new_population = elitism(population, 5)

            while len(new_population) < populationSize:

                parentA = RouletteWheelSelection(population)
                parentB = RouletteWheelSelection(population)
            
                child = singlePointCrossOver(parentA,parentB)

                child = bitFlipMutation(child,mutationRate)

                new_population.append(child)

            
            current_best_chromosome = elitism(new_population, 1)[0]
            current_best_cost = fitness(current_best_chromosome)

            print(f"Current chromosome {current_best_chromosome}")
            print(f"Current best cost is : {current_best_cost}")

            if current_best_cost > best_cost:
                best_cost = current_best_cost
                best_chromosome = current_best_chromosome
            
            population = new_population


        print(f"The best chromosome is : {best_chromosome}")
        print(f"The best fitness value is : {best_cost}")


GeneticAlgo(50,50,0.1)