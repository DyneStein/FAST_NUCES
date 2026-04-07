import random
import math

# ================================================================
#  THE DATA — same TSP city matrix as your SA code
#  city[i][j] = distance from city i to city j
#  City 0 is always start/end (fixed). We evolve the middle part.
# ================================================================

city = [
    [ 0, 12, 19,  8, 15, 22],
    [12,  0,  9, 14,  6, 18],
    [19,  9,  0, 11, 17,  5],
    [ 8, 14, 11,  0, 20, 13],
    [15,  6, 17, 20,  0, 10],
    [22, 18,  5, 13, 10,  0]
]

# ================================================================
#  COST FUNCTION — same as your SA
#  state = [1,2,3,4,5]  means route 0→1→2→3→4→5→0
# ================================================================

def route_cost(state, grid):
    route = [0] + state + [0]    # add city 0 at start and end
    total = 0
    for i in range(len(route) - 1):
        total = total + grid[route[i]][route[i+1]]
    return total

# ================================================================
#  FITNESS — GA maximises fitness, so we invert cost
#  lower cost = higher fitness
#  fitness = 1 / cost   (so fitness of 52 cost = 0.019)
# ================================================================

def fitness(state, grid):
    return 1 / route_cost(state, grid)


# ================================================================
#  INITIAL POPULATION
#
#  We create pop_size random individuals.
#  Each individual = a shuffled list of cities [1,2,3,4,5]
#  (city 0 is always start/end, not included in the gene)
#
#  Example for 5 cities (excluding city 0):
#  Individual 1: [2, 4, 1, 5, 3]
#  Individual 2: [5, 1, 3, 2, 4]
#  ... etc
# ================================================================

def generate_population(pop_size, num_cities):
    population = []

    for _ in range(pop_size):          # repeat pop_size times
        individual = list(range(1, num_cities))   
        # range(1, 6) = [1, 2, 3, 4, 5] — all cities except 0
        # list() converts range object into an actual list

        random.shuffle(individual)     # shuffle IN PLACE — scrambles the list randomly
        population.append(individual)  # add this individual to population

    return population
    # Returns e.g. [ [3,1,5,2,4], [2,4,1,3,5], [5,2,3,1,4], ... ]


# ================================================================
#  ---- SELECTION METHOD 1: TOURNAMENT ----
#
#  Step by step:
#  1. Pick k RANDOM indices from the population  (using random.sample)
#  2. Find which index has the HIGHEST fitness   (using max with key=)
#  3. Return that individual as the winner/parent
#
#  Example with k=3, population of 10:
#  population = [ind0, ind1, ind2, ind3, ind4, ind5, ind6, ind7, ind8, ind9]
#  random.sample(range(10), 3) might give [2, 7, 4]
#  We check fitness of ind2, ind7, ind4
#  Suppose ind7 has the highest fitness — return ind7
# ================================================================

def tournament_selection(population, grid, k=3):

    # random.sample(range(len(population)), k)
    # range(len(population)) = range(10) = [0,1,2,3,4,5,6,7,8,9]  — all valid indices
    # random.sample picks k=3 of these without repeats, e.g. [2, 7, 4]
    indices = random.sample(range(len(population)), k)

    # max(indices,  key = lambda i : fitness(population[i], grid))
    # For each index i in [2, 7, 4], compute fitness(population[i], grid)
    # Return the index i that produced the HIGHEST fitness score
    # lambda i : fitness(population[i], grid)
    #   → "given index i, return the fitness of population[i]"
    winner_idx = max(indices, key=lambda i: fitness(population[i], grid))

    # Return the actual individual (the list of cities), not just its index
    return population[winner_idx]


# ================================================================
#  ---- SELECTION METHOD 2: ROULETTE WHEEL ----
#
#  Step by step:
#  1. Compute total fitness of ALL individuals
#  2. Each individual's "slice" = its fitness / total fitness
#  3. Generate a random number r between 0 and 1
#  4. Walk through individuals accumulating their slices
#  5. The first one whose cumulative slice exceeds r is selected
#
#  Example:
#  fitnesses = [10, 5, 25, 10]   total = 50
#  slices    = [0.2, 0.1, 0.5, 0.2]
#  cumulative = [0.2, 0.3, 0.8, 1.0]
#  r = 0.55 → falls in range 0.3–0.8 → ind 2 (fitness 25) selected
# ================================================================

def roulette_selection(population, grid):

    # Step 1: compute ALL fitness scores
    # This is a list comprehension — same as:
    #   all_fitnesses = []
    #   for ind in population:
    #       all_fitnesses.append(fitness(ind, grid))
    all_fitnesses = [fitness(ind, grid) for ind in population]

    # Step 2: sum them all up
    total = sum(all_fitnesses)    # sum() adds every element in a list

    # Step 3: random float between 0.0 and 1.0
    r = random.random()

    # Step 4 & 5: walk through accumulating slices
    # enumerate(all_fitnesses) gives us (0, fit0), (1, fit1), (2, fit2) ...
    # i = index,  f = fitness value at that index
    cumulative = 0
    for i, f in enumerate(all_fitnesses):
        cumulative = cumulative + (f / total)   # add this individual's slice
        if r <= cumulative:
            return population[i]               # r landed in this individual's slice!

    return population[-1]   # fallback — floating point might cause r to just exceed 1.0
                            # population[-1] = last element in the list


# ================================================================
#  ---- SELECTION METHOD 3: ELITISM ----
#
#  Step by step:
#  1. Pair each individual with its fitness → list of (fitness, individual)
#  2. Sort that paired list, biggest fitness first
#  3. Return the top elite_count individuals (just the individuals, not fitness)
#
#  Example with elite_count=2:
#  population = [indA, indB, indC, indD]
#  fitnesses  = [0.02, 0.04, 0.01, 0.03]
#
#  zip(fitnesses, population) = [(0.02,indA), (0.04,indB), (0.01,indC), (0.03,indD)]
#  after list() = [(0.02,indA), (0.04,indB), (0.01,indC), (0.03,indD)]
#  after sort(reverse=True) = [(0.04,indB), (0.03,indD), (0.02,indA), (0.01,indC)]
#  top 2 = [(0.04,indB), (0.03,indD)]
#  extract just the individuals = [indB, indD]
# ================================================================

def get_elites(population, grid, elite_count=2):

    # list(zip(  [f0,f1,f2,f3],  [ind0,ind1,ind2,ind3]  ))
    # zip stitches them together: [(f0,ind0), (f1,ind1), (f2,ind2), ...]
    # list() makes it a real list (zip is lazy by default)
    all_fitnesses = [fitness(ind, grid) for ind in population]
    paired = list(zip(all_fitnesses, population))
    # paired is now: [(0.019, [1,4,2,5,3]),  (0.022, [3,1,5,2,4]),  ...]

    # sort by the first element of each tuple (the fitness)
    # reverse=True means biggest fitness first (descending)
    paired.sort(reverse=True)
    # paired is now sorted: [(0.022, [3,1,5,2,4]),  (0.019, [1,4,2,5,3]),  ...]

    # paired[:elite_count] = first elite_count items
    # for fit, ind in ...  unpacks each tuple into fit and ind
    # we only want ind (the individual), not fit (the fitness number)
    elites = [ind for fit, ind in paired[:elite_count]]
    # This list comprehension means:
    #   result = []
    #   for fit, ind in paired[:elite_count]:
    #       result.append(ind)

    return elites


# ================================================================
#  ---- CROSSOVER METHOD 1: SINGLE-POINT ----
#
#  Only works safely for NON-permutation problems (strings, bits).
#  Shown here for completeness and understanding.
#
#  Step by step:
#  1. Pick one random cut point
#  2. Child = left side of A  +  right side of B
#
#  Example:
#  A = [9, 3, 7, 1, 5, 2]   cut = 3
#  B = [4, 8, 2, 6, 0, 1]
#  Child = [9, 3, 7,  |  6, 0, 1]
#            A's left     B's right
# ================================================================

def single_point_crossover(parent_a, parent_b):
    size = len(parent_a)

    # randint(1, size-1) picks an integer between 1 and size-1 inclusive
    # We avoid 0 and size so the cut actually splits something
    cut = random.randint(1, size - 1)

    # parent_a[:cut] = everything before the cut point (left slice)
    # parent_b[cut:] = everything from cut to end (right slice)
    # + concatenates the two lists
    child = parent_a[:cut] + parent_b[cut:]

    return child
    # WARNING: may produce duplicates for TSP! Use OX for permutations.


# ================================================================
#  ---- CROSSOVER METHOD 2: TWO-POINT ----
#
#  Step by step:
#  1. Pick two random cut points (cut1 < cut2)
#  2. Child = outside of A  +  middle of B
#
#  Example:
#  A = [9, 3, 7, 1, 5, 2]   cut1=1, cut2=4
#  B = [4, 8, 2, 6, 0, 1]
#                 |         |
#  Child = [9,  |  8, 2, 6  |  2]
#           A[0]   B[1:4]     A[5]
#  = A[:1] + B[1:4] + A[4:]
#  = [9]   + [8,2,6] + [5,2]
#  = [9, 8, 2, 6, 5, 2]   ← again duplicate issues for TSP
# ================================================================

def two_point_crossover(parent_a, parent_b):
    size = len(parent_a)

    # Pick two distinct cut points
    cut1 = random.randint(1, size - 2)         # leave room for cut2
    cut2 = random.randint(cut1 + 1, size - 1)  # cut2 must be AFTER cut1

    # child = A's left  +  B's middle  +  A's right
    child = parent_a[:cut1] + parent_b[cut1:cut2] + parent_a[cut2:]

    return child


# ================================================================
#  ---- CROSSOVER METHOD 3: ORDER CROSSOVER (OX) ----
#  THE ONE TO USE FOR TSP — no duplicates guaranteed
#
#  Step by step:
#  1. Pick two cut points → defines a segment in parent A
#  2. Copy that segment into child at SAME positions
#  3. Fill remaining positions from parent B, reading B in order
#     starting from cut2+1 (wrapping around), SKIPPING cities
#     that are already in the child (i.e., in the copied segment)
#
#  Full example:
#  A = [1, 2, 3, 4, 5, 6, 7]   cut1=2, cut2=5  → segment = [3,4,5,6]
#  B = [3, 7, 5, 1, 6, 4, 2]
#
#  Step 2 — child after copying segment:
#  child = [?, ?, 3, 4, 5, 6, ?]   positions 0,1,6 are empty
#
#  Step 3 — read B starting at position cut2+1 = 6, wrapping:
#  B positions in reading order: 6,0,1,2,3,4
#  B values in that order:        2,3,7,5,1,6,4
#  Skip 3,4,5,6 (already in child): keep 2, keep 7, keep 1
#  Fill order = [2, 7, 1]
#
#  Step 4 — fill empty slots left to right:
#  pos 0 = 2,  pos 1 = 7,  pos 6 = 1
#  child = [2, 7, 3, 4, 5, 6, 1]  ← all 7 cities, no duplicates!
# ================================================================

def order_crossover(parent_a, parent_b):
    size = len(parent_a)

    # Step 1 — two random cut points
    cut1 = random.randint(0, size - 2)
    cut2 = random.randint(cut1 + 1, size - 1)

    # Step 2 — create child with Nones, copy segment from A
    # [None] * size = [None, None, None, None, None, None, None]
    child = [None] * size

    # child[cut1 : cut2+1] = parent_a[cut1 : cut2+1]
    # This copies the slice from A directly into the same positions in child
    child[cut1 : cut2+1] = parent_a[cut1 : cut2+1]
    # child is now e.g. [None, None, 3, 4, 5, 6, None]

    # Step 3 — figure out which cities are already placed (in the segment)
    # set() creates an unordered collection for fast lookup
    # child[cut1:cut2+1] = [3,4,5,6]  → segment_set = {3,4,5,6}
    segment_set = set(child[cut1 : cut2+1])

    # Build the reading order of B: start at cut2+1, go to end, then wrap to 0
    # Example: size=7, cut2=5 → reading positions: 6,0,1,2,3,4
    # range(cut2+1, size) = range(6, 7) = [6]
    # range(0, cut2+1)    = range(0, 6) = [0,1,2,3,4,5]
    # combined: [6, 0, 1, 2, 3, 4, 5]
    reading_order = list(range(cut2 + 1, size)) + list(range(0, cut2 + 1))

    # Filter B using this reading order, skipping cities already in segment
    # [parent_b[pos] for pos in reading_order if parent_b[pos] not in segment_set]
    # This is a list comprehension with a condition:
    #   result = []
    #   for pos in reading_order:
    #       if parent_b[pos] not in segment_set:
    #           result.append(parent_b[pos])
    b_values = [parent_b[pos] for pos in reading_order
                if parent_b[pos] not in segment_set]
    # b_values = the cities from B we need to fill, in the right order

    # Step 4 — fill the None slots in child from left to right using b_values
    b_idx = 0   # our pointer into b_values
    for i in range(size):
        if child[i] is None:           # found an empty slot
            child[i] = b_values[b_idx] # fill it with next value from B
            b_idx = b_idx + 1          # advance the b_values pointer

    return child


# ================================================================
#  ---- MUTATION: SWAP MUTATION ----
#
#  With probability mutation_rate, randomly swap two genes.
#  For permutations (TSP) this is SAFE — no duplicates introduced.
#
#  Example:
#  individual = [2, 7, 3, 4, 5, 6, 1]   mutation_rate = 0.1
#  random.random() = 0.07  → 0.07 < 0.1 → DO mutate
#  pick i=1, j=4  (random indices)
#  swap positions 1 and 4:
#  result = [2, 5, 3, 4, 7, 6, 1]
# ================================================================

def swap_mutation(individual, mutation_rate=0.1):
    # random.random() returns a float in [0.0, 1.0)
    # if it's less than mutation_rate, we mutate
    if random.random() < mutation_rate:
        # random.sample(range(len(individual)), 2) picks 2 DIFFERENT indices
        # e.g. range(7) = [0,1,2,3,4,5,6], sample 2 → [1, 4]
        i, j = random.sample(range(len(individual)), 2)
        # i, j = unpacks the list of 2 into two variables

        # Python swap — no temp variable needed
        individual[i], individual[j] = individual[j], individual[i]

    return individual


# ================================================================
#  THE MAIN GA LOOP — puts everything together
#
#  Parameters you can tune:
#  pop_size      = how many individuals per generation (50–200)
#  generations   = how many iterations to run (200–1000)
#  mutation_rate = probability of mutation per child (0.05–0.15)
#  elite_count   = how many best individuals survive unchanged (1–3)
#  tournament_k  = how many contestants per tournament (2–5)
#  selection     = 'tournament' or 'roulette'
#  crossover     = 'ox' (order) or 'two_point' or 'single_point'
# ================================================================

def GeneticAlgorithm(grid,
                     pop_size=50,
                     generations=400,
                     mutation_rate=0.1,
                     elite_count=2,
                     tournament_k=3,
                     selection='tournament',
                     crossover='ox'):

    num_cities = len(grid)   # = 6 for our matrix

    # ---- STEP 1: Create initial random population ----
    population = generate_population(pop_size, num_cities)

    best_individual = None
    best_cost = float('inf')   # infinity — any real cost will be less than this

    print("=" * 60)
    print(f"  GA started")
    print(f"  Selection : {selection}   Crossover : {crossover}")
    print(f"  Pop size  : {pop_size}    Generations: {generations}")
    print(f"  Mutation  : {mutation_rate}   Elites: {elite_count}")
    print("=" * 60)

    for gen in range(generations):

        # ---- STEP 2: Elitism — copy best N individuals unchanged ----
        # get_elites returns e.g. [[3,1,5,2,4], [1,4,2,5,3]]
        new_population = get_elites(population, grid, elite_count)

        # ---- STEP 3: Fill rest of new population ----
        while len(new_population) < pop_size:

            # --- 3a: Select two parents ---
            if selection == 'tournament':
                parent_a = tournament_selection(population, grid, k=tournament_k)
                parent_b = tournament_selection(population, grid, k=tournament_k)
            else:  # roulette
                parent_a = roulette_selection(population, grid)
                parent_b = roulette_selection(population, grid)

            # --- 3b: Crossover to make a child ---
            if crossover == 'ox':
                child = order_crossover(parent_a, parent_b)
            elif crossover == 'two_point':
                child = two_point_crossover(parent_a, parent_b)
            else:  # single_point
                child = single_point_crossover(parent_a, parent_b)

            # --- 3c: Maybe mutate the child ---
            child = swap_mutation(child, mutation_rate)

            new_population.append(child)

        # ---- STEP 4: Replace old population with new one ----
        population = new_population

        # ---- STEP 5: Track the best solution found so far ----
        # Find the current generation's best
        current_best = get_elites(population, grid, 1)[0]
        current_cost = route_cost(current_best, grid)

        if current_cost < best_cost:
            best_cost = current_cost
            best_individual = current_best[:]   # .copy() so we don't lose it later
            print(f"  Gen {gen:>4} | New best: {[0]+best_individual+[0]} | Cost: {best_cost}")

    print("=" * 60)
    print(f"  DONE")
    print(f"  Best route : {[0] + best_individual + [0]}")
    print(f"  Best cost  : {best_cost}")
    print("=" * 60)
    return best_individual, best_cost


# ================================================================
#  RUN 4 DIFFERENT COMBINATIONS so you can compare
# ================================================================

print("\n\n--- RUN 1: Tournament + OX (recommended combo) ---")
GeneticAlgorithm(city, selection='tournament', crossover='ox')

print("\n\n--- RUN 2: Roulette + OX ---")
GeneticAlgorithm(city, selection='roulette', crossover='ox')

print("\n\n--- RUN 3: Tournament + Two-point (not ideal for TSP but works sometimes) ---")
GeneticAlgorithm(city, selection='tournament', crossover='two_point')

print("\n\n--- RUN 4: Tournament + OX, higher mutation (more exploration) ---")
GeneticAlgorithm(city, selection='tournament', crossover='ox',
                 mutation_rate=0.3, pop_size=80, generations=400)
