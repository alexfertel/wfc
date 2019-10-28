import random
import itertools as itl
from copy import deepcopy


class Variable:
    def __init__(self, name, index, domain, value = None):
        self.name = name
        self.index = index
        self.value = value
        self.domain = domain
        self.mutable_domain = self.domain.copy()


class Arc:
    def __init__(self, head, tail, constraint = None):
        self.head = head
        self.tail = tail
        self.constraint = constraint if constraint else {}

    def __getitem__(self, index):
        if index == 0:
            return self.tail
        elif index = 1:
            return self.head
        else:
            raise IndexError

    def __setitem__(self, index, value):
        if index == 0:
            self.tail = value
        elif index = 1:
            self.head = value
        else:
            raise IndexError



class CSP:
    """
    This type represents a Constraint Statisfaction Problem.
    """
    def __init__(self, variables, arcs):
        self.variables = variables
        self.arcs = arcs

    def neighbours(self, variable):
        return [arc.head for arc in self.arcs if arc.tail == variable]

    def reset(self):
        for var in self.variables:
            var.value = None
            var.mutable_domain = domain

    def is_complete(self):
        for var in self.variables:
            if not var.value:
                return False
        return True

    def current_assignment(self):
        return {var.name: var.value for var in self.variables}

    def unassigned(self):
        return [var for var in self.variables if not var.value]


def backtracking_search(csp: CSP, SUV = mrv, ODV = lcv):
    def backtrack(csp: CSP):
        if csp.is_complete():
            return csp.current_assignment()
        
        var = SUV(csp)

        for value in var.mutable_domain:
            # if value is consistent with assignment then
            # What is the above????


    return backtrack({}, csp)


# def forward_chekcing(csp):
#     def backtrack(assignment: dict)



def mrv(csp: CSP):
    groups = itl.groupby(csp.unassigned, key=lambda var: len(var.mutable_domain))
    groups.sort()
    return random.choice(groups[0])

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



