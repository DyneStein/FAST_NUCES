import copy

#variables list
variables = ["WA","NT","SA","Q"]

#this is basically the initial domain for every variable
domains = {
    "WA" : ["Red","Green","Blue"],
    "NT":["Red","Green","Blue"],
    "SA":["Red","Green","Blue"],
    "Q":["Red","Green","Blue"]
}


#now, neighbours here mean variables linked with BINARY CONSTRAINTS (there can be any constraint e.g x>y OR WT!=SA (meaning there color can not be equal))
neighbours = {
    "WA" : ["NT","SA"],
    "NT": ["WA","SA","Q"],
    "SA" :["WA", "NT","Q"],
    "Q" : ["NT","SA"]
}


#This is the constraint function so for example
# in this case we only have one type of constraint 
# we can have multiple TYPES of constriants
def constraint(VarA, ValueOfVarA, VarB, ValueOfVarB):
    return ValueOfVarA != ValueOfVarB #so this is the constraint that varA and varB should not have same values and it should be satisfied


#Unassigned 
#MRV --> minimum Remaining Value, basically returns that UNASSIGNED variable which has the minimum AMOUNT of LEGAL values (i.e does not violate any constraint with already-assigned variables) in its DOMAIN
#when there is a tie, MRV uses degree heuristic to select the one which has greater degree (i.e more neighbours)
def MRV(Current_assignment, domains):

    unassigned =[]

    for v in variables:
        if v not in Current_assignment:
            unassigned.append(v)


    mrv_var = None
    smallest_domain = 999 #ye wo legal values wali domain hai

    for v in unassigned:
        if len(domains[v]) < smallest_domain:
            smallest_domain = len(domains[v])
            mrv_var = v
        
    return mrv_var



#LCV--> basically it returns that value which has minimum constriants conflicts with neighbour variable's domain values. so 
# a value with minimum conflicting constraints would cause minimum amount of removal of values from neighbour variable's domain
def LCV(var,domains):

    values  = domains[var]
    score = {}

    #is variable ki domain me tu kaafi values ho sakti haina
    for value in values:
        conflict_count = 0

        for neighbour in neighbours[var]:

            for neighbour_value in domains[neighbour]:

                if not constraint(var, value, neighbour, neighbour_value):
                    conflict_count+=1

        score[value] = conflict_count
    
    values.sort(key=lambda x:score[x])

    return values


#Unassigned 
#FC--> domain pruning for neighbour variables the specific value selected from LCV and specific variable comming from MRV
def FC(var, value, domains , assignment):
    new_domain = copy.deepcopy(domains)
    
    for neighbour in neighbours[var]:
        
        if neighbour not in assignment:
            
            valid = []

            for v in new_domain[neighbour]:

                if constraint(var,value,neighbour,v):
                    valid.append(v)

            new_domain[neighbour] = valid

            #why this (this would even return for asingle neighbour) ?
            if len(valid) == 0:
                return None

    return new_domain
            

#here the daddy function starts which is ARC consistency AC3
#ARC CONSISTENCY :
#For every value of Xi
#there exists a compatible value in Xj

#AC3 tend to run before main CSP search 
#like reducing overall domain before searching for solution
# as a preprocessing or cleaning
#thats why in AC3 we removes values from original domain




"""

# THE PROBLEM: Modifying a list while looping over it

domains["SA"] = ["Red", "Green", "Blue"]

# WITHOUT [:]  ← BUGGY
for value in domains["SA"]:        # loop uses the SAME list
    domains["SA"].remove(value)    # shrinking the same list mid-loop

# Step 1: pointer at index 0 → value = "Red"   → remove "Red"
# list is now ["Green", "Blue"]
# Step 2: pointer at index 1 → value = "Blue"  → "Green" was SKIPPED!
# Step 3: loop ends (only 2 items left, pointer goes out)

print(domains["SA"])  # ["Green"]  ← Green was never checked! BUG


# ─────────────────────────────────────────────

# WITH [:]  ← CORRECT
domains["SA"] = ["Red", "Green", "Blue"]  # reset

for value in domains["SA"][:]:     # loop walks a FROZEN COPY ["Red","Green","Blue"]
    domains["SA"].remove(value)    # modifies the ORIGINAL, loop is unaffected

# Step 1: copy says index 0 = "Red"   → remove "Red"   from original
# Step 2: copy says index 1 = "Green" → remove "Green" from original
# Step 3: copy says index 2 = "Blue"  → remove "Blue"  from original

print(domains["SA"])  # []  ← all values were visited correctly

"""




def revise(Xi, Xj, domains):
    revised = False

    for Xi_value in domains[Xi][:]:

        found = False

        for Xj_value in domains[Xj]:

            if constraint(Xi,Xi_value, Xj,Xj_value):
                found = True
                break
    
        if not found:
            #Modifying original domain
            domains[Xi].remove(Xi_value)
            revised = True
    
    return revised



def AC3(domains):

    queue = []

    for Xi in variables:
        for Xj in neighbours[Xi]:
            queue.append((Xi,Xj))


    while queue:
        (Xi,Xj) = queue.pop(0)
        if revise(Xi,Xj,domains):

            if len(domains[Xi])==0:
                return False
            
            for Xk in neighbours[Xi]:
                if Xk != Xj:
                    queue.append((Xk,Xi))
    return True




def backtrack(assignment, domains, method):

    # GOAL TEST
    if len(assignment) == len(variables):
        return assignment


    # SELECT VARIABLE (MRV)
    var = MRV(assignment, domains)


    # ORDER VALUES (LCV)
    values = LCV(var, domains)


    for value in values:

        legal = True

        # check constraint with already assigned neighbours
        for neighbour in neighbours[var]:

            if neighbour in assignment:

                if not constraint(var, value, neighbour, assignment[neighbour]):
                    legal = False
                    break


        if legal:

            # assign value
            assignment[var] = value

            # copy domains
            new_domains = copy.deepcopy(domains)

            new_domains[var] = [value]


            # FORWARD CHECKING
            if method == "FC":

                new_domains = FC(var, value, new_domains, assignment)

                if new_domains is None:

                    del assignment[var]
                    continue


            # AC3
            if method == "AC3":

                if not AC3(new_domains):

                    del assignment[var]
                    continue


            # RECURSIVE SEARCH
            result = backtrack(assignment, new_domains, method)

            if result is not None:
                return result


            # BACKTRACK
            del assignment[var]


    return None





#This is fully manually done without any function in C++ style
"""
def backtrack(assignment, domains, method):

    # -----------------------------
    # STEP 1 : Check if solution complete
    # -----------------------------
    if len(assignment) == len(variables):

        return assignment


    # -----------------------------
    # STEP 2 : Select variable using MRV
    # -----------------------------
    selected_variable = None
    smallest_domain_size = 999

    for variable in variables:

        if variable not in assignment:

            domain_size = len(domains[variable])

            if domain_size < smallest_domain_size:

                smallest_domain_size = domain_size
                selected_variable = variable


    var = selected_variable


    # -----------------------------
    # STEP 3 : Order values using LCV
    # -----------------------------
    value_scores = {}

    for value in domains[var]:

        conflict_count = 0

        for neighbor in neighbors[var]:

            for neighbor_value in domains[neighbor]:

                if not constraint(var, value, neighbor, neighbor_value):

                    conflict_count += 1

        value_scores[value] = conflict_count


    ordered_values = sorted(domains[var], key=lambda v: value_scores[v])


    # -----------------------------
    # STEP 4 : Try each value
    # -----------------------------
    for value in ordered_values:


        # -----------------------------
        # STEP 4A : Check consistency
        # -----------------------------
        is_valid = True

        for neighbor in neighbors[var]:

            if neighbor in assignment:

                neighbor_value = assignment[neighbor]

                if not constraint(var, value, neighbor, neighbor_value):

                    is_valid = False
                    break


        if is_valid == False:

            continue


        # -----------------------------
        # STEP 4B : Assign value
        # -----------------------------
        assignment[var] = value


        # -----------------------------
        # STEP 4C : Copy domains
        # -----------------------------
        new_domains = {}

        for variable in domains:

            new_domains[variable] = []

            for v in domains[variable]:

                new_domains[variable].append(v)


        new_domains[var] = [value]


        # -----------------------------
        # STEP 4D : Filtering
        # -----------------------------
        if method == "FC":

            new_domains = forward_check(var, value, new_domains, assignment)

            if new_domains is None:

                del assignment[var]
                continue


        if method == "AC3":

            success = AC3(new_domains)

            if success == False:

                del assignment[var]
                continue


        # -----------------------------
        # STEP 4E : Recurse
        # -----------------------------
        result = backtrack(assignment, new_domains, method)

        if result is not None:

            return result


        # -----------------------------
        # STEP 4F : Backtrack
        # -----------------------------
        del assignment[var]


    # -----------------------------
    # STEP 5 : Failure
    # -----------------------------
    return None



"""
#During MRV, if there is a tie, then pick the variable with higher degree... (Degree Hueristic)


#NOTES made with AI


# ============================================================
# AC-3 (Arc Consistency 3) - Complete Notes
# ============================================================

# WHAT IS AC-3?
# AC-3 is a constraint propagation algorithm used in Constraint
# Satisfaction Problems (CSPs). It enforces arc consistency by
# pruning values from variable domains that cannot possibly be
# part of any valid solution.

# ------------------------------------------------------------
# INITIAL SETUP
# ------------------------------------------------------------
# - AC-3 starts by pushing all arcs in both directions into a queue.
# - For every constrained pair (X, Y), both (X, Y) and (Y, X) are added.
# - This means every variable-pair relationship is checked from both sides.

# ------------------------------------------------------------
# THE REVISE STEP - CORE LOGIC
# ------------------------------------------------------------
# For each arc (X, Y) popped from the queue:
# - Go through every value vx in X's domain.
# - Check if there is at least one value vy in Y's domain that satisfies the constraint.
# - If no value in Y is consistent with vx, remove vx from X's domain.
# - This is called "revising" the arc.

# ------------------------------------------------------------
# RE-ADDING NEIGHBORS (PROPAGATION)
# ------------------------------------------------------------
# - After processing arc (X, Y), ONLY IF X's domain shrank,
#   re-add arcs (Z, X) for every neighbor Z of X, excluding Y.
# - If X's domain did NOT shrink, nothing changed so no need to re-check neighbors.
# - This propagation is what makes AC-3 powerful.
#   A change in one variable ripples through the network.

# ------------------------------------------------------------
# TERMINATION CONDITIONS
# ------------------------------------------------------------
# AC-3 stops under two conditions:
# - FAILURE : A domain becomes empty -> return failure, no solution exists.
# - SUCCESS : The queue becomes empty with all domains non-empty
#             -> arc consistency achieved.

# ------------------------------------------------------------
# THE 3 POSSIBLE OUTCOMES
# ------------------------------------------------------------
# 1. A domain becomes empty
#    Meaning  : No solution exists.
#    Next Step: Return failure immediately.
#
# 2. All domains have exactly 1 value
#    Meaning  : Unique solution found directly.
#    Next Step: Done, read off the solution.
#
# 3. Some domains still have 2+ values
#    Meaning  : Inconclusive, ambiguity remains.
#    Next Step: Run backtracking search on the pruned domains.

# ------------------------------------------------------------
# IMPORTANT LIMITATION
# ------------------------------------------------------------
# - AC-3 is NOT a complete solver. It is a filter/pruning step.
# - It checks pairs of variables in isolation,
#   NOT combinations of 3 or more simultaneously.
# - So even if arc consistency is achieved,
#   a global solution may or may not exist.
# - In practice, AC-3 is used inside backtracking search.
#   This combination is called MAC (Maintaining Arc Consistency).
# - After every variable assignment during search,
#   AC-3 is re-run to prune domains further.

# ------------------------------------------------------------
# KEY TAKEAWAY
# ------------------------------------------------------------
# AC-3 reduces the search space by eliminating obviously inconsistent values,
# but it cannot always solve the problem on its own.
# The real power comes from combining it with backtracking search.

# ============================================================