# import random

class CSP:
    """
    This type represents a Constraint Statisfaction Problem.
    """
    def __init__(self, variables, arcs, domains, constraints):
        self.variables = variables
        self.arcs = arcs
        self.domains = domains
        self.constraints = constraints


def backtracking_search(csp: CSP, SUV = mrv, ODV = lcv):
    def backtrack(assignment: dict, csp: CSP):
        if len(assignment) == len(csp.variables):
            return assignment
        
        var = SUV(csp, assignment)



    return backtrack({}, csp)

def mrv(csp: CSP, assignment: dict):
    unassigned = [var for var in csp.variables if not var in assignment]
    domains = [csp.domains[var] for var in unassigned]
    pairs = list(zip(unassigned, domains))
    pairs.sort(key=lambda x: len(x[1]))
  
    # Maybe insert a random here when choosing between tied pairs.
    return pairs[0][0]

def lcv(csp: CSP, var: int):
    pass


def ac3(csp: CSP):
    q = list(csp.arcs)

    if q:
        (i, j) = q.pop()
        
        if revise(csp, (i, j)):
            if not csp.domains[i]: return False

            for k in [k for (l, k) in csp.arcs if l == i and k != j]:
                q.append((k, i))
    
    return True

def revise(csp: CSP, vars: tuple):
    (i, j) = vars
    revised = False
    for x in csp.domains[i].copy():
        # if no value y in D j allows (x ,y) to satisfy the constraint between X i and X j then
        allowed = csp.constraints[(i, j)]
        satisfies = False
        for y in csp.domains[j]:
            if (x, y) in allowed:
                satisfies = True
        
        if not satisfies:
            print((x, y))
            csp.domains[i].remove(x)
            revised = True

    return revised



