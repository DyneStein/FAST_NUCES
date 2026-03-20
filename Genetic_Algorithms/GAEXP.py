import random
import math


# ================================================================
#  ENCODING — HOW CHROMOSOMES ARE REPRESENTED
#
#  YOUR CODE (Permutation Encoding) — used for TSP:
#    individual = [2, 4, 1, 5, 3]
#    means: route 0 → 2 → 4 → 1 → 5 → 3 → 0
#    every city appears EXACTLY ONCE — it's a permutation
#
#  PDF APPROACH (Value / Integer Encoding) — used for math problems:
#    chromosome = [a, b, c, d] = [9, 3, 7, 4]
#    each gene is an independent integer value, not a position
#    genes CAN repeat — [3, 3, 7, 4] is perfectly valid
#
#  ┌─────────────────────┬──────────────────┬────────────────────────┐
#  │ Encoding Type       │ Use When         │ Example Problem        │
#  ├─────────────────────┼──────────────────┼────────────────────────┤
#  │ Permutation         │ ordering matters │ TSP, job scheduling    │
#  │ Value / Integer     │ independent vars │ f(a,b,c,d) = 3a+2b+... │
#  │ Binary              │ yes/no decisions │ knapsack problem       │
#  │ Real-valued (float) │ continuous space │ neural net weights     │
#  └─────────────────────┴──────────────────┴────────────────────────┘
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
#  COST FUNCTION (same as your original — no change needed)
# ================================================================

def route_cost(state, grid):
    route = [0] + state + [0]
    total = 0
    for i in range(len(route) - 1):
        total = total + grid[route[i]][route[i+1]]
    return total


# ================================================================
#  FITNESS FUNCTION — THIS IS WHERE MAXIMIZATION VS MINIMIZATION SPLITS
#
#  YOUR CODE: fitness = 1 / cost
#    → lower cost  = higher fitness  (inverts the cost into fitness)
#    → GA always MAXIMISES fitness internally
#    → this is the standard trick for minimization problems in GA
#
#  PDF MAXIMIZATION APPROACH: fitness = f_obj directly
#    → the objective function value IS the fitness
#    → works when higher objective = better solution
#    → example: f(a,b,c,d) = 3a + 2b + 5c + 4d  → bigger f = better
#    → Fitness[i] = F_obj[i]   (no transformation needed)
#
#  PDF MINIMIZATION APPROACH: fitness = 1 / (1 + f_obj)
#    → works when lower objective = better solution
#    → +1 in denominator avoids division-by-zero when f_obj = 0
#    → example: f_obj=0 → fitness=1.0  (perfect),  f_obj=99 → fitness=0.01
#    → YOUR CODE uses 1/cost which is same idea but without the +1
#      (safe because TSP cost is always > 0, never exactly 0)
#
#  WHICH TO USE:
#    - Maximization problem?   → fitness = f_obj  (direct)
#    - Minimization problem?   → fitness = 1/(1 + f_obj)  (inverted)
#    - TSP / permutation?      → fitness = 1/cost  (same as minimization trick)
# ================================================================

def fitness(state, grid):
    # YOUR CODE: inversion trick — TSP is minimization, so lower cost = higher fitness
    return 1 / route_cost(state, grid)


# --- PDF MAXIMIZATION fitness (shown separately for comparison) ---
# def fitness_maximization(chromosome):
#     a, b, c, d = chromosome
#     return 3*a + 2*b + 5*c + 4*d          # fitness IS the objective directly
#
# --- PDF MINIMIZATION fitness (shown separately for comparison) ---
# def fitness_minimization(chromosome):
#     x, y, z = chromosome
#     f_obj = (x + 2*y + 3*z - 20) ** 2     # compute how far we are from target
#     return 1 / (1 + f_obj)                # invert: smaller f_obj → bigger fitness


# ================================================================
#  INITIAL POPULATION
#
#  YOUR CODE: shuffled permutations — every individual is a random
#    ordering of cities [1,2,3,4,5]
#    random.shuffle(individual) scrambles the list IN PLACE
#
#  PDF APPROACH: random integer values per gene
#    each gene is independently drawn from the valid range
#    e.g. chromosome = [random(0,10), random(0,10), random(0,10), random(0,10)]
#
#  KEY DIFFERENCE:
#    Permutation init:  shuffle a fixed set  → no duplicates guaranteed
#    Value init:        randint per gene      → duplicates perfectly fine
# ================================================================

def generate_population(pop_size, num_cities):
    population = []
    for _ in range(pop_size):
        # YOUR APPROACH: permutation — shuffle [1,2,3,4,5]
        individual = list(range(1, num_cities))
        # list(range(1, 6)) = [1, 2, 3, 4, 5]
        # range() creates a lazy sequence; list() forces it into a real list
        random.shuffle(individual)  # shuffles the list in-place, returns None
        population.append(individual)
    return population


# --- PDF APPROACH for value-encoded problems (shown for comparison) ---
# def generate_population_value_encoded(pop_size, num_genes, gene_min, gene_max):
#     population = []
#     for _ in range(pop_size):
#         # each gene is independently random — duplicates allowed
#         individual = [random.randint(gene_min, gene_max) for _ in range(num_genes)]
#         # list comprehension: builds list by running randint num_genes times
#         # e.g. num_genes=4, range 0-10 → [7, 2, 9, 1]
#         population.append(individual)
#     return population


# ================================================================
#  ════════════════════════════════════════════════════════════════
#                     S E L E C T I O N
#  ════════════════════════════════════════════════════════════════
#
#  BIG PICTURE — WHY THE PDFs AND YOUR CODE LOOK DIFFERENT:
#
#  PDF PIPELINE (Generational Replacement):
#    Step 1: Selection → rebuild ENTIRE population (N new chromosomes)
#              uses roulette to pick N chromosomes for the new pool
#    Step 2: Crossover → each chromosome in new pool rolls R vs ρc
#              if R < ρc → mark as parent candidate
#              pair up all marked candidates sequentially
#              only marked pairs cross over; others pass through unchanged
#    Step 3: Mutation → flatten population into one long gene array
#              pick random positions globally, replace gene values
#    Result: entire old population is REPLACED at once
#
#  YOUR CODE PIPELINE (Steady-State with Elitism):
#    Step 1: Elitism → copy top N individuals directly to new population
#    Step 2: Loop until new population is full:
#              call selection TWICE to get two parents
#              ALWAYS cross over (no crossover rate gate)
#              maybe mutate the child
#    Result: new population is built child by child; elites always survive
#
#  ┌────────────────────────┬────────────────────────┬──────────────────────┐
#  │ Aspect                 │ PDF (Generational)     │ Your Code (Elitism)  │
#  ├────────────────────────┼────────────────────────┼──────────────────────┤
#  │ Selection role         │ Rebuild full population│ Pick 2 parents/child │
#  │ Selection method       │ Roulette only          │ Tournament / Roulette│
#  │ Crossover trigger      │ R < ρc per chromosome  │ Always (rate=1.0)    │
#  │ Best solution safety   │ Can be lost            │ Elitism guarantees   │
#  │ Population replacement │ All at once            │ Child by child       │
#  │ Best for               │ Teaching / textbooks   │ Real problems / TSP  │
#  └────────────────────────┴────────────────────────┴──────────────────────┘
# ================================================================


# ================================================================
#  SELECTION METHOD 1: TOURNAMENT  ← YOUR CODE'S DEFAULT
#
#  HOW IT WORKS:
#    1. Pick k random individuals from the population
#    2. Return whichever one has the highest fitness
#    — like a mini competition: only k contestants, winner advances
#
#  SYNTAX BREAKDOWN:
#    random.sample(range(len(population)), k)
#      → range(len(population)) = all valid indices, e.g. range(50) = [0..49]
#      → random.sample picks k of them WITHOUT replacement (no duplicates)
#      → e.g. k=3 might give [12, 37, 5]
#
#    max(indices, key=lambda i: fitness(population[i], grid))
#      → max() finds the largest value in a collection
#      → key= tells max() WHAT to compare — here it computes fitness for each index
#      → lambda i: fitness(population[i], grid)
#           lambda = anonymous function with no name
#           i      = the input parameter (one index at a time)
#           body   = fitness(population[i], grid)  (what to return)
#      → max() runs this lambda for each i in [12, 37, 5],
#           picks the i that gives the biggest fitness
#
#  BEST FOR:
#    - TSP, scheduling, any permutation problem
#    - Large populations
#    - When you want controllable selection pressure (adjust k)
#    - k=2: low pressure (weak tournament), k=7: high pressure (strong tournament)
#
#  NOT IN PDFs: PDFs only show roulette. Tournament is a more modern approach.
# ================================================================

def tournament_selection(population, grid, k=3):
    indices = random.sample(range(len(population)), k)
    # random.sample returns a list of k unique indices
    # e.g. [2, 7, 4]

    winner_idx = max(indices, key=lambda i: fitness(population[i], grid))
    # max scans [2, 7, 4], computes fitness for population[2], population[7], population[4]
    # returns the index with highest fitness — not the fitness value itself, the INDEX

    return population[winner_idx]
    # return the actual individual list (e.g. [3,1,5,2,4]), not just the index


# ================================================================
#  SELECTION METHOD 2: ROULETTE WHEEL  ← PDF METHOD (all 3 PDFs)
#
#  HOW IT WORKS:
#    1. Compute fitness of every individual
#    2. Each individual's "slice" = fitness / total_fitness
#    3. Spin the wheel (generate random r in [0,1])
#    4. Walk cumulative slices; whoever's slice r lands in is selected
#
#  SYNTAX BREAKDOWN:
#    [fitness(ind, grid) for ind in population]
#      → list comprehension: runs fitness() for every ind in population
#      → equivalent to a for loop that appends each result
#      → produces e.g. [0.019, 0.022, 0.017, ...]
#
#    enumerate(all_fitnesses)
#      → gives (index, value) pairs: (0, 0.019), (1, 0.022), ...
#      → lets you track both the value and its position simultaneously
#
#  PDF EXACT PROCEDURE:
#    P[i] = Fitness[i] / Total       ← probability per chromosome
#    C[i] = sum of P[1..i]           ← cumulative probability
#    Generate R in [0,1]
#    If C[i-1] < R ≤ C[i] → select chromosome i
#
#  BEST FOR:
#    - Value-encoded problems (math optimization)
#    - When fitness values are well-spread (not too close together)
#
#  WEAKNESS:
#    - If one chromosome dominates (e.g. fitness 1000 vs others at 1),
#      it gets selected almost every time → premature convergence
#    - Negative fitness values break it (not an issue here but worth knowing)
# ================================================================

def roulette_selection(population, grid):
    all_fitnesses = [fitness(ind, grid) for ind in population]
    # list comprehension builds the fitness list in one line
    # same as:  all_fitnesses = []
    #           for ind in population: all_fitnesses.append(fitness(ind, grid))

    total = sum(all_fitnesses)
    # sum() adds every element: sum([0.019, 0.022, 0.017]) = 0.058

    r = random.random()
    # random.random() → float in [0.0, 1.0)
    # this is the "spin" of the roulette wheel

    cumulative = 0
    for i, f in enumerate(all_fitnesses):
        # enumerate gives: i=0 f=0.019, then i=1 f=0.022, etc.
        cumulative = cumulative + (f / total)
        # f/total = this individual's slice of the wheel
        # cumulative grows: 0.019/total, then 0.041/total, etc.
        if r <= cumulative:
            return population[i]
            # r landed in this individual's slice — return it

    return population[-1]
    # population[-1] = last element (Python negative index = from the end)
    # fallback only needed due to floating-point rounding (cumulative might be 0.9999...)


# ================================================================
#  SELECTION METHOD 3: RANK SELECTION  ← NOT IN PDFs, NOT IN YOUR CODE
#
#  HOW IT WORKS:
#    1. Sort population by fitness (worst=rank 1, best=rank N)
#    2. Assign selection probability based on RANK not actual fitness
#    3. Run roulette on these rank-based probabilities
#
#  WHY IT EXISTS:
#    Solves roulette's "dominant chromosome" problem
#    Even if best fitness = 1000x the worst, rank difference is always just N-1
#    Prevents premature convergence while still being fitness-proportionate
#
#  BEST FOR:
#    - Problems where fitness values are very uneven in scale
#    - Middle ground between roulette (fitness-biased) and tournament
# ================================================================

def rank_selection(population, grid):
    # Step 1: sort population worst-to-best fitness
    # sorted() returns a NEW sorted list (doesn't modify original)
    # key=lambda ind: fitness(ind, grid) → sort by fitness value
    # reverse=False → ascending (worst first, so rank 1 = worst)
    sorted_pop = sorted(population, key=lambda ind: fitness(ind, grid), reverse=False)

    n = len(sorted_pop)
    # ranks = [1, 2, 3, ..., n]   (worst gets rank 1, best gets rank n)
    ranks = list(range(1, n + 1))
    # range(1, n+1) = [1, 2, 3, ..., n]

    total_rank = sum(ranks)
    # total_rank = n*(n+1)/2   (sum of 1 to n)

    r = random.random()
    cumulative = 0
    for i, rank in enumerate(ranks):
        cumulative += rank / total_rank
        # probability proportional to rank, not raw fitness
        if r <= cumulative:
            return sorted_pop[i]

    return sorted_pop[-1]


# ================================================================
#  ELITISM  ← YOUR CODE ONLY (not in PDFs)
#
#  HOW IT WORKS:
#    1. Pair each individual with its fitness
#    2. Sort descending by fitness
#    3. Return top elite_count individuals unchanged
#
#  WHY YOUR CODE HAS IT BUT PDFs DON'T:
#    PDFs teach the basic generational GA where the whole population
#    is replaced each generation — the best CAN be lost by bad luck.
#    Elitism is a modern improvement: it GUARANTEES the best solution
#    found so far is never lost.
#
#  SYNTAX BREAKDOWN:
#    zip(all_fitnesses, population)
#      → stitches two lists together element by element
#      → zip([f0,f1,f2], [ind0,ind1,ind2]) = [(f0,ind0),(f1,ind1),(f2,ind2)]
#      → lazy by default — list() forces it to actually compute
#
#    paired.sort(reverse=True)
#      → .sort() modifies the list IN PLACE (no new list created)
#      → sorts tuples by first element (fitness) since tuples compare left-to-right
#      → reverse=True = descending = highest fitness first
#
#    [ind for fit, ind in paired[:elite_count]]
#      → paired[:elite_count] = first elite_count tuples
#      → for fit, ind in ... = unpack each tuple into two variables
#      → we keep only ind (the chromosome), discard fit (the number)
#
#  BEST FOR: Almost always beneficial — very low cost, big safety guarantee
#  RISK: Too many elites → population stagnates (keep elite_count small: 1-3)
# ================================================================

def get_elites(population, grid, elite_count=2):
    all_fitnesses = [fitness(ind, grid) for ind in population]
    paired = list(zip(all_fitnesses, population))
    # zip stitches fitness to its chromosome: [(0.019,[3,1,5,2,4]), ...]
    # list() forces the lazy zip into a real list in memory

    paired.sort(reverse=True)
    # sort by first element of tuple (fitness), biggest first

    elites = [ind for fit, ind in paired[:elite_count]]
    # slice first elite_count items, extract just the chromosome (ind)
    return elites


# ================================================================
#  ════════════════════════════════════════════════════════════════
#                      C R O S S O V E R
#  ════════════════════════════════════════════════════════════════
#
#  PDF CROSSOVER TRIGGER (ρc-based):
#    Each chromosome rolls R vs crossover_rate ρc
#    if R < ρc → mark as parent candidate
#    Collect all marked chromosomes, pair them up (1st+2nd, 3rd+4th, ...)
#    Odd one out? It stays unchanged (no partner)
#
#    PDF pseudocode:
#      for each chromosome k:
#          R[k] = random(0,1)
#          if R[k] < ρc:
#              mark chromosome[k] as parent
#      pair marked chromosomes sequentially and cross them
#
#  YOUR CODE CROSSOVER TRIGGER:
#    No ρc gate — you just ALWAYS cross two selected parents
#    This is equivalent to ρc = 1.0 (100% crossover rate)
#    Simpler and more common in modern implementations
#
#  BELOW: both PDF-style and modern implementation shown for each type
# ================================================================


# ================================================================
#  CROSSOVER TYPE 1: ONE-POINT  ← PDF METHOD (all 3 PDFs use this)
#
#  HOW IT WORKS:
#    Pick one random cut position
#    Child 1 = left of A  +  right of B
#    Child 2 = left of B  +  right of A
#
#  EXAMPLE:
#    A = [2, 8, 3, 5]   cut = 2
#    B = [7, 1, 6, 2]
#    Child1 = [2, 8 | 6, 2]   (A's left + B's right)
#    Child2 = [7, 1 | 3, 5]   (B's left + A's right)
#
#  BEST FOR: value-encoded chromosomes (integer, binary, float genes)
#  WARNING:  UNSAFE for permutations! [2, 8, 6, 2] has duplicate 2
#            Never use single-point for TSP — use OX instead
#
#  SYNTAX:
#    random.randint(1, size-1)
#      → returns integer between 1 and size-1 INCLUSIVE
#      → avoids cut=0 (would give empty left side) or cut=size (empty right)
#    parent_a[:cut] = elements from index 0 up to (not including) cut
#    parent_b[cut:] = elements from cut to the end
#    + operator on lists = concatenation (join two lists)
# ================================================================

def single_point_crossover(parent_a, parent_b):
    size = len(parent_a)
    cut = random.randint(1, size - 1)
    # randint is INCLUSIVE on both ends: randint(1, 5) can give 1,2,3,4, or 5

    child = parent_a[:cut] + parent_b[cut:]
    # parent_a[:cut] = left slice of A (indices 0 to cut-1)
    # parent_b[cut:] = right slice of B (indices cut to end)
    # + joins them into one list
    return child
    # WARNING: produces duplicates for TSP! Only use for value-encoded genes.


# --- PDF-style: produce BOTH children (the PDF always swaps both ways) ---
def single_point_crossover_both_children(parent_a, parent_b):
    size = len(parent_a)
    cut = random.randint(1, size - 1)
    child1 = parent_a[:cut] + parent_b[cut:]   # A-left + B-right
    child2 = parent_b[:cut] + parent_a[cut:]   # B-left + A-right  ← PDF also makes this
    return child1, child2
    # your code only uses child1; PDFs replace BOTH parents with their children


# ================================================================
#  CROSSOVER TYPE 2: TWO-POINT  ← YOUR CODE (for non-TSP use)
#
#  HOW IT WORKS:
#    Pick two cut points (cut1 < cut2)
#    Child = A's left + B's middle + A's right
#
#  EXAMPLE:
#    A = [9, 3, 7, 1, 5, 2]   cut1=1, cut2=4
#    B = [4, 8, 2, 6, 0, 1]
#    Child = A[:1] + B[1:4] + A[4:] = [9] + [8,2,6] + [5,2] = [9,8,2,6,5,2]
#
#  BEST FOR: value-encoded chromosomes (better mixing than single-point)
#  WARNING:  Still unsafe for permutations (same duplicate problem)
#
#  SYNTAX:
#    cut1 = random.randint(1, size-2)   → leave room: need at least 1 spot after cut1
#    cut2 = random.randint(cut1+1, size-1)  → cut2 must be STRICTLY after cut1
# ================================================================

def two_point_crossover(parent_a, parent_b):
    size = len(parent_a)
    cut1 = random.randint(1, size - 2)
    # size-2 because cut2 = cut1+1 at minimum, must be ≤ size-1

    cut2 = random.randint(cut1 + 1, size - 1)
    # cut1+1 ensures cut2 > cut1 (no empty middle segment)

    child = parent_a[:cut1] + parent_b[cut1:cut2] + parent_a[cut2:]
    # A's left:   parent_a[:cut1]       = elements 0 to cut1-1
    # B's middle: parent_b[cut1:cut2]   = elements cut1 to cut2-1
    # A's right:  parent_a[cut2:]       = elements cut2 to end
    return child


# ================================================================
#  CROSSOVER TYPE 3: ORDER CROSSOVER (OX)  ← YOUR CODE'S DEFAULT
#
#  HOW IT WORKS:
#    1. Copy a segment from A directly into child at same positions
#    2. Fill remaining slots using B's values in circular order,
#       skipping values already in the copied segment
#
#  EXAMPLE:
#    A = [1, 2, 3, 4, 5, 6, 7]   cut1=2, cut2=5
#    B = [3, 7, 5, 1, 6, 4, 2]
#    Step 1 → child = [?, ?, 3, 4, 5, 6, ?]   (segment from A)
#    Step 2 → read B from cut2+1 circularly: positions 6,0,1,2,3,4
#             B values in that order: 2, 3, 7, 5, 1, 6, 4
#             skip {3,4,5,6} (already placed) → keep: 2, 7, 1
#    Step 3 → fill empty slots left-to-right: [2, 7, 3, 4, 5, 6, 1]
#
#  WHY IT'S SAFE FOR TSP:
#    The segment guarantees a block of cities, and B fills the rest
#    WITHOUT repeating any city. No duplicates ever possible.
#
#  NOT IN PDFs: PDFs use simple integer genes, so one-point is fine.
#    OX was invented specifically for permutation problems like TSP.
#
#  BEST FOR: TSP, job scheduling, any problem where order matters
#            and every item must appear exactly once
#
#  SYNTAX:
#    [None] * size
#      → creates a list of `size` None values: [None, None, None, ...]
#      → None is Python's "nothing here" placeholder
#    child[cut1 : cut2+1] = parent_a[cut1 : cut2+1]
#      → slice assignment: copy multiple elements at once
#      → cut2+1 because Python slices are [start, end) — end is exclusive
#    set(child[cut1 : cut2+1])
#      → set() creates an unordered collection with NO duplicates
#      → used for fast "is this city already placed?" lookup
#      → checking "x in set" is O(1) vs O(n) for a list
#    list(range(cut2+1, size)) + list(range(0, cut2+1))
#      → builds the circular reading order of B
#      → e.g. size=7, cut2=5 → [6, 0, 1, 2, 3, 4, 5]
# ================================================================

def order_crossover(parent_a, parent_b):
    size = len(parent_a)
    cut1 = random.randint(0, size - 2)
    cut2 = random.randint(cut1 + 1, size - 1)

    child = [None] * size
    # [None]*5 = [None, None, None, None, None]
    # We'll fill in real values step by step

    child[cut1 : cut2+1] = parent_a[cut1 : cut2+1]
    # slice assignment copies the segment from A into child
    # cut2+1 because Python slices DON'T include the end index

    segment_set = set(child[cut1 : cut2+1])
    # set for O(1) lookup — "is this city already in the child?"

    reading_order = list(range(cut2 + 1, size)) + list(range(0, cut2 + 1))
    # circular order: start reading B from cut2+1, wrap to 0
    # range(cut2+1, size) = positions AFTER cut in B
    # range(0, cut2+1)    = positions from start up to cut in B
    # + joins them into one circular sequence

    b_values = [parent_b[pos] for pos in reading_order
                if parent_b[pos] not in segment_set]
    # filter B: keep only cities not already in the segment
    # not in segment_set → O(1) check per city

    b_idx = 0
    for i in range(size):
        if child[i] is None:            # empty slot found
            child[i] = b_values[b_idx]  # fill with next city from B
            b_idx = b_idx + 1           # advance pointer into b_values

    return child


# ================================================================
#  CROSSOVER TYPE 4: UNIFORM CROSSOVER  ← NOT IN PDFs, NOT IN YOUR CODE
#
#  HOW IT WORKS:
#    For each gene position, flip a coin (50/50)
#    Heads → take gene from A
#    Tails → take gene from B
#
#  EXAMPLE:
#    A = [2, 8, 3, 5]
#    B = [7, 1, 6, 2]
#    Coin flips: [H, T, H, T]
#    Child = [2, 1, 3, 2]   (positions 0,2 from A; positions 1,3 from B)
#
#  BEST FOR: problems where genes are independent and order doesn't matter
#  WARNING:  Unsafe for permutations (same duplicate problem as single-point)
# ================================================================

def uniform_crossover(parent_a, parent_b):
    child = []
    for gene_a, gene_b in zip(parent_a, parent_b):
        # zip pairs up corresponding genes: (gene_a[0], gene_b[0]), etc.
        if random.random() < 0.5:
            child.append(gene_a)  # 50% chance: take from A
        else:
            child.append(gene_b)  # 50% chance: take from B
    return child


# ================================================================
#  ════════════════════════════════════════════════════════════════
#                       M U T A T I O N
#  ════════════════════════════════════════════════════════════════
#
#  ┌─────────────────────┬───────────────────────────┬───────────────────────┐
#  │ Mutation Type       │ What it does              │ Best for              │
#  ├─────────────────────┼───────────────────────────┼───────────────────────┤
#  │ Random Resetting    │ Replace gene with new rand │ Value/integer encoded │
#  │ (PDF method)        │ value from valid range     │ math problems         │
#  ├─────────────────────┼───────────────────────────┼───────────────────────┤
#  │ Swap Mutation       │ Swap two genes in same     │ Permutations (TSP)    │
#  │ (YOUR CODE)         │ chromosome                 │ ordering problems     │
#  ├─────────────────────┼───────────────────────────┼───────────────────────┤
#  │ Inversion Mutation  │ Reverse a sub-segment      │ Permutations (TSP)    │
#  │ (not in either)     │ of the chromosome          │ better than swap      │
#  ├─────────────────────┼───────────────────────────┼───────────────────────┤
#  │ Insertion Mutation  │ Move one gene to a new     │ Permutations (TSP)    │
#  │ (not in either)     │ random position            │ fine-tuning routes    │
#  └─────────────────────┴───────────────────────────┴───────────────────────┘
#
#  PDF TRIGGER (Population-level):
#    total_gen = genes_per_chromosome * population_size
#    num_mutations = round(mutation_rate * total_gen)
#    generate num_mutations random integers in [1, total_gen]
#    each integer maps to a specific chromosome + gene position
#    replace that gene with a new random value
#
#    How to map position → chromosome and gene:
#      chromosome_index = ceil(position / genes_per_chromosome) - 1
#      gene_index       = position - chromosome_index * genes_per_chromosome - 1
#
#  YOUR CODE TRIGGER (Per-chromosome):
#    For each individual: generate R in [0,1]
#    if R < mutation_rate → mutate (swap two genes)
#    This is simpler and applied per-child as it's created
# ================================================================


# ================================================================
#  MUTATION METHOD 1: SWAP MUTATION  ← YOUR CODE
#
#  HOW IT WORKS:
#    Pick two random positions i and j
#    Swap the genes at those positions
#
#  WHY SAFE FOR PERMUTATIONS:
#    Swapping never adds or removes values — same cities, different order
#    [2,7,3,4,5,6,1] → swap positions 1 and 4 → [2,5,3,4,7,6,1] ✓
#    Both lists have same values, just rearranged
#
#  SYNTAX:
#    random.sample(range(len(individual)), 2)
#      → picks 2 DIFFERENT indices (no repeating same index)
#      → returns a list: [i, j]
#    i, j = [i, j]
#      → tuple unpacking: assigns list elements to variables
#    individual[i], individual[j] = individual[j], individual[i]
#      → Python simultaneous swap — evaluates RIGHT side first
#      → no temp variable needed (unlike C/C++ where you need a temp)
#      → in C++: int temp = arr[i]; arr[i] = arr[j]; arr[j] = temp;
# ================================================================

def swap_mutation(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        # random.random() = float in [0.0, 1.0)
        # if this float < mutation_rate, we mutate
        i, j = random.sample(range(len(individual)), 2)
        # random.sample with k=2 → guaranteed i ≠ j
        individual[i], individual[j] = individual[j], individual[i]
        # Python's simultaneous swap — no temp variable needed
    return individual


# ================================================================
#  MUTATION METHOD 2: RANDOM RESETTING  ← PDF METHOD (all 3 PDFs)
#
#  HOW IT WORKS (PDF population-level approach):
#    1. total_gen = genes_per_chromosome * pop_size
#    2. num_mutations = round(mutation_rate * total_gen)
#    3. Generate num_mutations random integers in [1, total_gen]
#    4. Map each integer to: which chromosome, which gene
#    5. Replace that gene with a new random value in [gene_min, gene_max]
#
#  WHY UNSAFE FOR PERMUTATIONS:
#    [2,4,1,5,3] → mutate position 2 → [2,4,2,5,3] ← city 2 appears twice!
#    City 1 is now missing — invalid TSP route
#
#  BEST FOR: Value-encoded chromosomes (integers, floats, anything non-permutation)
# ================================================================

def pdf_style_mutation(population, mutation_rate, gene_min, gene_max, genes_per_chromosome):
    # PDF APPROACH: operate on the ENTIRE population at once
    pop_size = len(population)
    total_gen = genes_per_chromosome * pop_size
    # total_gen = total number of individual genes across ALL chromosomes
    # e.g. 4 genes each, 6 chromosomes → total_gen = 24

    num_mutations = round(mutation_rate * total_gen)
    # expected number of genes to mutate
    # round() goes to nearest integer (0.1 * 24 = 2.4 → 2)

    for _ in range(num_mutations):
        pos = random.randint(1, total_gen)
        # pos is a 1-based global position across ALL genes
        # e.g. pos=7 with 4 genes/chromosome: chromosome 2 (floor division), gene 3

        # Map position to chromosome index and gene index
        # Using ceiling division: chromosome = ceil(pos / genes_per_chromosome) - 1
        chrom_idx = math.ceil(pos / genes_per_chromosome) - 1
        # math.ceil(7/4) = ceil(1.75) = 2 → chromosome index = 2-1 = 1 (0-based)

        gene_idx = pos - chrom_idx * genes_per_chromosome - 1
        # gene_idx = 7 - 1*4 - 1 = 2 (0-based gene position within chromosome)

        # Replace gene with new random value in valid range
        population[chrom_idx][gene_idx] = random.randint(gene_min, gene_max)
        # randint is INCLUSIVE: randint(0, 10) can produce 0 or 10

    return population


# ================================================================
#  MUTATION METHOD 3: INVERSION MUTATION  ← NOT IN PDFs OR YOUR CODE
#
#  HOW IT WORKS:
#    Pick two random positions, REVERSE the sub-segment between them
#
#  EXAMPLE:
#    individual = [2, 7, 3, 4, 5, 6, 1]   i=2, j=5
#    segment = [3, 4, 5, 6]   reversed = [6, 5, 4, 3]
#    result  = [2, 7, 6, 5, 4, 3, 1]
#
#  WHY SAFE FOR PERMUTATIONS:
#    Reversing a sub-segment just rearranges existing values
#    All cities still appear exactly once
#
#  BEST FOR: TSP — often finds better routes than swap mutation
#    because it can "undo" a crossing path (2-opt style improvement)
#
#  SYNTAX:
#    individual[i:j+1] = individual[i:j+1][::-1]
#      → individual[i:j+1] = sub-list from i to j inclusive
#      → [::-1] = reverse using step=-1 (go backwards through the list)
#      → slice assignment replaces that segment in-place
# ================================================================

def inversion_mutation(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = sorted(random.sample(range(len(individual)), 2))
        # sorted() ensures i < j (so we get a valid segment)
        # random.sample gives 2 unique indices in any order
        # sorted() puts them in ascending order: i ≤ j always

        individual[i:j+1] = individual[i:j+1][::-1]
        # individual[i:j+1] = the segment to reverse
        # [::-1] reverses it: [3,4,5,6] → [6,5,4,3]
        # assignment puts reversed segment back into the same positions
    return individual


# ================================================================
#  MUTATION METHOD 4: INSERTION MUTATION  ← NOT IN PDFs OR YOUR CODE
#
#  HOW IT WORKS:
#    Pick a random gene, remove it, insert it at another random position
#
#  EXAMPLE:
#    individual = [2, 7, 3, 4, 5, 6, 1]
#    remove index 2 → gene=3, remaining=[2, 7, 4, 5, 6, 1]
#    insert 3 at position 5 → [2, 7, 4, 5, 6, 3, 1]
#
#  SAFE FOR PERMUTATIONS: just moves one element, nothing added or removed
#  BEST FOR: fine-tuning near the end of evolution (small local changes)
#
#  SYNTAX:
#    individual.pop(i)
#      → removes element at index i AND returns it
#      → list shrinks by 1
#    individual.insert(j, gene)
#      → inserts gene at position j, shifting everything right
#      → list grows by 1 back to original size
# ================================================================

def insertion_mutation(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i = random.randint(0, len(individual) - 1)
        gene = individual.pop(i)
        # .pop(i) removes AND returns the element at index i
        # individual is now 1 shorter

        j = random.randint(0, len(individual))
        # j can be len(individual) to insert at the very end
        individual.insert(j, gene)
        # .insert(j, gene) places gene at position j
        # everything at j and beyond shifts one position right
    return individual


# ================================================================
#  ════════════════════════════════════════════════════════════════
#           PDF-STYLE CROSSOVER TRIGGER (ρc-based)
#  ════════════════════════════════════════════════════════════════
#
#  This function implements exactly what the PDFs describe:
#    each chromosome in the population rolls R vs ρc
#    those with R < ρc become parents
#    parents are paired sequentially and crossed over
#
#  YOUR CODE skips this entirely — it always crosses two selected parents.
#  The PDF approach gives more control but is more complex to implement.
#
#  WHEN TO USE PDF APPROACH:
#    - When you want explicit control over how many crossovers happen per gen
#    - In textbook/academic implementations
#  WHEN TO USE YOUR CODE'S APPROACH:
#    - Modern implementations — simpler, more predictable
#    - When using elitism (you're filling exactly pop_size - elite_count slots)
# ================================================================

def pdf_style_crossover_phase(population, crossover_rate, crossover_fn):
    # Step 1: each chromosome rolls against crossover_rate
    parent_candidates = []
    non_parents = []

    for chromosome in population:
        r = random.random()
        if r < crossover_rate:
            parent_candidates.append(chromosome)
            # R < ρc → this chromosome wants to mate
        else:
            non_parents.append(chromosome)
            # R ≥ ρc → this chromosome passes through unchanged

    # Step 2: pair up candidates (1st with 2nd, 3rd with 4th, ...)
    new_offspring = []
    i = 0
    while i + 1 < len(parent_candidates):
        # need at least 2 remaining to form a pair
        child1, child2 = crossover_fn(parent_candidates[i], parent_candidates[i+1])
        new_offspring.append(child1)
        new_offspring.append(child2)
        i = i + 2
        # i += 2 skips past the pair we just processed

    # If odd number of parents, last one has no partner → passes through
    if i < len(parent_candidates):
        new_offspring.append(parent_candidates[i])

    # Step 3: combine offspring + non-parents to form new population
    return new_offspring + non_parents


# ================================================================
#  THE MAIN GA LOOP — YOUR CODE + PDF COMPARISON AT EVERY STEP
#
#  YOUR CODE: Steady-State with Elitism
#    1. Copy elites directly
#    2. Loop: select parents → crossover → mutate → add child
#    3. Replace old population entirely
#
#  PDF CODE: Generational Replacement
#    1. Roulette selection rebuilds entire population
#    2. ρc-based crossover on new population
#    3. Population-level mutation using global gene positions
#    4. Entire old population replaced
#
#  Parameters you can tune:
#    pop_size      = 50–200 (larger = more diversity, slower per generation)
#    generations   = 200–1000 (more = better solution, more time)
#    mutation_rate = 0.05–0.15 (too high = random walk, too low = stagnation)
#    elite_count   = 1–3 (more = safer but less diversity)
#    tournament_k  = 2–5 (higher = stronger selection pressure)
#    selection     = 'tournament' (TSP) or 'roulette' (math problems)
#    crossover     = 'ox' (TSP) or 'single_point'/'two_point' (value-encoded)
#    mutation_type = 'swap' (TSP) or 'inversion' (TSP better) or 'reset' (value)
# ================================================================

def GeneticAlgorithm(grid,
                     pop_size=50,
                     generations=400,
                     mutation_rate=0.1,
                     elite_count=2,
                     tournament_k=3,
                     selection='tournament',
                     crossover='ox',
                     mutation_type='swap'):

    num_cities = len(grid)

    # ---- STEP 1: Initialize population ----
    # YOUR CODE: permutation encoding — shuffled lists of cities
    # PDF CODE:  value encoding — random integers per gene
    population = generate_population(pop_size, num_cities)

    best_individual = None
    best_cost = float('inf')
    # float('inf') = positive infinity — any real number will be less than this
    # used as a "worst possible" starting value for comparison

    print("=" * 60)
    print(f"  GA started")
    print(f"  Selection : {selection}   Crossover : {crossover}")
    print(f"  Mutation  : {mutation_type}   Pop: {pop_size}   Gens: {generations}")
    print("=" * 60)

    for gen in range(generations):

        # ---- STEP 2: Elitism (YOUR CODE ONLY — not in PDFs) ----
        # PDFs: no elitism — entire population gets replaced (best can be lost)
        # Your code: top elite_count individuals carried forward unchanged
        new_population = get_elites(population, grid, elite_count)
        # new_population starts with [best_ind, 2nd_best_ind, ...]

        # ---- STEP 3: Fill rest of new population ----
        # YOUR CODE: select parents on demand, always crossover, maybe mutate
        # PDF CODE:  selection already done (rebuilt population in step above)
        #            then crossover by ρc gate, then global mutation pass
        while len(new_population) < pop_size:

            # --- 3a: Select two parents ---
            # YOUR CODE: calls selection function directly to get each parent
            # PDF CODE:  parents come from ρc-filtered roulette-selected pool

            if selection == 'tournament':
                parent_a = tournament_selection(population, grid, k=tournament_k)
                parent_b = tournament_selection(population, grid, k=tournament_k)
                # tournament: each parent is winner of its own k-contestant competition
                # two separate tournaments → two (potentially different) parents

            elif selection == 'roulette':
                parent_a = roulette_selection(population, grid)
                parent_b = roulette_selection(population, grid)
                # roulette: spin the wheel twice, independently
                # same chromosome could be selected twice (fine — and expected sometimes)

            else:  # rank
                parent_a = rank_selection(population, grid)
                parent_b = rank_selection(population, grid)

            # --- 3b: Crossover ---
            # YOUR CODE: always crossover (no ρc gate)
            # PDF CODE:  only crossover if both parents rolled R < ρc

            if crossover == 'ox':
                child = order_crossover(parent_a, parent_b)
                # BEST for TSP — no duplicates guaranteed, preserves relative order

            elif crossover == 'two_point':
                child = two_point_crossover(parent_a, parent_b)
                # OK for value-encoded; risky for TSP due to duplicates

            elif crossover == 'uniform':
                child = uniform_crossover(parent_a, parent_b)
                # gene-by-gene random mix; best for independent value genes

            else:  # single_point
                child = single_point_crossover(parent_a, parent_b)
                # simplest; OK for value-encoded, unsafe for TSP

            # --- 3c: Mutation ---
            # YOUR CODE: per-child swap mutation
            # PDF CODE:  population-level random resetting mutation

            if mutation_type == 'swap':
                child = swap_mutation(child, mutation_rate)
                # BEST for TSP — swaps two cities, no duplicates

            elif mutation_type == 'inversion':
                child = inversion_mutation(child, mutation_rate)
                # BETTER than swap for TSP — reverses a sub-segment
                # can undo crossing paths (2-opt style local improvement)

            elif mutation_type == 'insertion':
                child = insertion_mutation(child, mutation_rate)
                # moves one city to a new position — small local change

            # 'reset' (PDF mutation) is handled by pdf_style_mutation()
            # separately on the whole population, not per-child

            new_population.append(child)

        # ---- STEP 4: Replace old population ----
        # YOUR CODE: new_population replaces old entirely
        # PDF CODE:  same — new generation replaces old generation
        population = new_population

        # ---- STEP 5: Track best solution ----
        current_best = get_elites(population, grid, 1)[0]
        # get_elites(... 1) returns a list of 1 → [0] gets that one individual

        current_cost = route_cost(current_best, grid)

        if current_cost < best_cost:
            best_cost = current_cost
            best_individual = current_best[:]
            # [:] = shallow copy of the list
            # necessary because lists are mutable — without copy,
            # best_individual would point to same object as current_best
            # and could change later when the population is modified
            print(f"  Gen {gen:>4} | New best: {[0]+best_individual+[0]} | Cost: {best_cost}")

    print("=" * 60)
    print(f"  DONE")
    print(f"  Best route : {[0] + best_individual + [0]}")
    print(f"  Best cost  : {best_cost}")
    print("=" * 60)
    return best_individual, best_cost


# ================================================================
#  WHICH COMBO WORKS BEST FOR WHICH PROBLEM?
#
#  ┌──────────────────────────┬───────────────┬───────────────┬────────────────┐
#  │ Problem Type             │ Selection     │ Crossover     │ Mutation       │
#  ├──────────────────────────┼───────────────┼───────────────┼────────────────┤
#  │ TSP (your code)          │ Tournament    │ Order (OX)    │ Swap/Inversion │
#  │ Math maximization (PDF2) │ Roulette      │ Single-point  │ Random reset   │
#  │ Math minimization (PDF3) │ Roulette      │ Single-point  │ Random reset   │
#  │ Large-scale TSP          │ Tournament    │ Order (OX)    │ Inversion      │
#  │ Noisy fitness landscape  │ Rank          │ Order (OX)    │ Swap           │
#  │ Binary/knapsack          │ Tournament    │ Uniform       │ Bit-flip       │
#  └──────────────────────────┴───────────────┴───────────────┴────────────────┘
#
#  GOLDEN RULES:
#    1. Permutation problem? → ALWAYS use OX crossover + swap/inversion mutation
#    2. Value-encoded problem? → single/two-point crossover + random resetting
#    3. Fitness values very uneven? → rank selection over roulette
#    4. Want to guarantee best is never lost? → add elitism (elite_count=1-2)
#    5. Need more exploration? → lower tournament_k OR higher mutation_rate
#    6. Need more exploitation? → higher tournament_k OR lower mutation_rate
# ================================================================


# ---- RUN COMPARISONS ----

print("\n--- RUN 1: Tournament + OX + Swap  (YOUR ORIGINAL — best for TSP) ---")
GeneticAlgorithm(city, selection='tournament', crossover='ox', mutation_type='swap')

print("\n--- RUN 2: Roulette + OX + Swap  (PDF selection style + permutation ops) ---")
GeneticAlgorithm(city, selection='roulette', crossover='ox', mutation_type='swap')

print("\n--- RUN 3: Tournament + OX + Inversion  (better mutation than swap for TSP) ---")
GeneticAlgorithm(city, selection='tournament', crossover='ox', mutation_type='inversion')

print("\n--- RUN 4: Rank + OX + Swap  (protects against one dominant chromosome) ---")
GeneticAlgorithm(city, selection='rank', crossover='ox', mutation_type='swap')

print("\n--- RUN 5: Tournament + OX + Insertion  (fine-tuning style mutation) ---")
GeneticAlgorithm(city, selection='tournament', crossover='ox', mutation_type='insertion')
