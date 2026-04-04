import random
import math


city = [
    [ 0, 12, 19,  8, 15, 22],
    [12,  0,  9, 14,  6, 18],
    [19,  9,  0, 11, 17,  5],
    [ 8, 14, 11,  0, 20, 13],
    [15,  6, 17, 20,  0, 10],
    [22, 18,  5, 13, 10,  0]
]

def route_cost(state, grid):
    route = [0] + state + [0]
    total = 0
    for i in range(len(route) - 1):
        total += grid[route[i]][route[i+1]]
    return total

def fitness(state, grid):
    return 1 / route_cost(state, grid)

def generate_population(pop_size, num_cities):
    population = []
    for _ in range(pop_size):
        individual = list(range(1, num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

# ---- All your existing (GA_Full_Explained.py) selection / crossover / mutation functions ----
# (tournament_selection, roulette_selection, order_crossover, swap_mutation, etc.)
# UNCHANGED — paste them here as-is.

# ================================================================
#  FIND WORST — needed so we know who to replace
#
#  Same logic as get_elites, but reversed:
#  sort ascending by fitness (lowest = worst), return index 0
# ================================================================

def get_worst_index(population, grid):
    all_fitnesses = [fitness(ind, grid) for ind in population]
    paired = list(enumerate(all_fitnesses))        # [(0, f0), (1, f1), ...]
    paired.sort(key=lambda x: x[1])               # ascending: worst first
    return paired[0][0]                            # index of worst individual


# ================================================================
#  STEADY-STATE GA — the only function that changes meaningfully
#
#  Key differences vs generational:
#
#  1. No new_population list — we mutate the SAME population in place
#  2. Loop count = iterations, not "generations" (each step = 1 replacement)
#  3. After making a child, we find the WORST individual in the population
#  4. We only replace the worst if the child is strictly better
#     (this is called "elitist replacement" — the population never degrades)
#
#  Common iteration counts:
#  Generational: generations × pop_size  total evaluations
#  Steady-state: to match, set iterations = generations × pop_size
#  (e.g. 400 gens × 50 pop = 20,000 iterations)
# ================================================================

def SteadyStateGA(grid,
                  pop_size=50,
                  iterations=20000,       # ← replaces "generations"
                  mutation_rate=0.1,
                  tournament_k=3,
                  selection='tournament',
                  crossover='ox'):

    num_cities = len(grid)
    population = generate_population(pop_size, num_cities)

    best_individual = None
    best_cost = float('inf')

    print("=" * 60)
    print(f"  Steady-State GA started")
    print(f"  Selection: {selection}   Crossover: {crossover}")
    print(f"  Pop size : {pop_size}    Iterations: {iterations}")
    print("=" * 60)

    for it in range(iterations):

        # ---- STEP 1: Select two parents ----
        if selection == 'tournament':
            parent_a = tournament_selection(population, grid, k=tournament_k)
            parent_b = tournament_selection(population, grid, k=tournament_k)
        else:
            parent_a = roulette_selection(population, grid)
            parent_b = roulette_selection(population, grid)

        # ---- STEP 2: Make exactly ONE child ----
        if crossover == 'ox':
            child = order_crossover(parent_a, parent_b)
        elif crossover == 'two_point':
            child = two_point_crossover(parent_a, parent_b)
        else:
            child = single_point_crossover(parent_a, parent_b)

        child = swap_mutation(child, mutation_rate)

        # ---- STEP 3: Replace worst only if child is better ----
        # This is the ENTIRE difference from the generational version.
        worst_idx = get_worst_index(population, grid)

        if route_cost(child, grid) < route_cost(population[worst_idx], grid):
            population[worst_idx] = child          # in-place replacement

        # ---- STEP 4: Track best ----
        child_cost = route_cost(child, grid)
        if child_cost < best_cost:
            best_cost = child_cost
            best_individual = child[:]
            print(f"  Iter {it:>6} | New best: {[0]+best_individual+[0]} | Cost: {best_cost}")

    print("=" * 60)
    print(f"  DONE")
    print(f"  Best route : {[0] + best_individual + [0]}")
    print(f"  Best cost  : {best_cost}")
    print("=" * 60)
    return best_individual, best_cost


SteadyStateGA(city, selection='tournament', crossover='ox')