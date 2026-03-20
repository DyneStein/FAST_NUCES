import random
ChromosomeLength = 5
pop_size = 50




def fitness(value):
    return value**2

def generate_random_chromosome():
    chromosome=list(random.choice([0,1]) for i in range(ChromosomeLength))
    return chromosome

def chromosomeToDecimal(chromosome):
    #str.join is new to me to have a full fledge loop with str.join
    #str.join does NOT modify the string in place
    toString = "".join(str(bit) for bit in chromosome)
    return int(toString,2)


def fitnessValue(chromosome):
    value = chromosomeToDecimal(chromosome)
    return value*value


def generate_initial_population(size):
    pop = []
    for i in range(size):
        pop.append(generate_random_chromosome())
    
    return pop



def RouletteWheel(population):

    Fitnesses = [fitnessValue(ind) for ind in population]

    totalFitness = sum(Fitnesses)

    r = random.random()

    cummulativefitness = 0
    for i, f in enumerate(Fitnesses):
        cummulativefitness = cummulativefitness + (f/1+totalFitness)
        if r < cummulativefitness:
            return population[i]
    
    return population[-1] #last value returning if no r < any commulative value



def crossOver(parentA, parentB):

    size = len(parentA)

    cut = random.randint(1, size - 1)

    child = [None]*size

    for i in range(0,cut):
        child[i] = parentA[i]


    for i in range(cut,size):
        child[i] = parentB[i]

    return child




def mutationBitFlip(child, mutationRate):
    for i in range(len(child)):
        if random.random()<mutationRate:
            child[i] = 1-child[i]
    
    return child




def elitism(population, eliteSize):
    Fitnesses = [fitnessValue(chromosome) for chromosome in population]
    #zip it self returns an iterator not a list 
    #manually have to convert into list
    paired = list(zip(Fitnesses,population))
    paired.sort(reverse = True)
    elite = [chromosome for f,chromosome in paired[:eliteSize]]
    return elite




def geneticAlgo(GenerationSize, populationSize , mutationRate):

    population = generate_initial_population(populationSize)
    
    best_chromosome = []
    best_cost = 0

    for i in range(GenerationSize):

        new_population = elitism(population, 5)

        while len(new_population) < pop_size:
            
            #selection of parents
            parentA = RouletteWheel(population)
            parentB = RouletteWheel(population)

            #crossOver and child
            child = crossOver(parentA, parentB)

            #mutation of child
            child = mutationBitFlip(child,mutationRate)

            new_population.append(child)

        current_best_chromosome = elitism(new_population,1)[0]
        current_best_cost = fitnessValue(current_best_chromosome)

        if current_best_cost > best_cost:
            best_cost = current_best_cost
            best_chromosome = current_best_chromosome

        population = new_population
    

    print(f"The best chromosome is : {best_chromosome}")
    print("Best x:", chromosomeToDecimal(best_chromosome))
    print(f"The best cost is : {best_cost}")



geneticAlgo(1,1,0.05)















































