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

    def __str__(self):
        return f"var {self.index} - {self.name} - {self.domain} - {self.mutable_domain}"

    def __repr__(self):
        return self.name

class Arc:
    def __init__(self, head, tail, constraint = None):
        self.head = head
        self.tail = tail
        self.constraint = constraint if constraint else []

    def __getitem__(self, index):
        if index == 0:
            return self.tail
        elif index == 1:
            return self.head
        else:
            raise IndexError

    def __setitem__(self, index, value):
        if index == 0:
            self.tail = value
        elif index == 1:
            self.head = value
        else:
            raise IndexError

    def __str__(self):
        return f"arc {self.tail} --> {self.head} | {self.constraint}"

    def __repr__(self):
        return f"({repr(self.tail)} --> {repr(self.head)})"


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

    def get_var(self, index):
        for var in self.variables:
            if var.index == index:
                return var
        raise Exception("Var not found!")

    def get_arc(self, i, j):
        for arc in self.arcs:
            if arc.tail.index == i and arc.head.index == j:
                return arc
        raise Exception("Arc not found!")


# def forward_chekcing(csp):
#     def backtrack(assignment: dict)



def mrv(csp: CSP):
    groups = itl.groupby(csp.unassigned, key=lambda var: len(var.mutable_domain))
    groups.sort()
    return random.choice(groups[0])

def lcv(csp: CSP, var: int):
    pass


def ac3(csp: CSP):
    q = deepcopy(csp.arcs)

    if q:
        arc = q.pop()
        
        if revise(csp, arc):
            if not len(arc.tail.mutable_domain): return False

            for neighbour in csp.neighbours(arc.tail):
                if neighbour.index != arc.head.index:
                    q.append(csp.get_arc(neighbour, arc.tail))
    
    return True

def revise(csp: CSP, arc: Arc):
    revised = False
    for x in arc.tail.mutable_domain.copy():
        # if no value y in D j allows (x ,y) to satisfy the constraint between X i and X j then
        satisfies = False
        for y in arc.head.mutable_domain:
            if (x, y) in arc.constraint:
                satisfies = True
        
        if not satisfies:
            print((x, y))
            arc.tail.mutable_domain.remove(x)
            revised = True

    return revised

def backtracking_search(csp: CSP, SUV = mrv, ODV = lcv):
    def backtrack(csp: CSP):
        if csp.is_complete():
            return csp.current_assignment()
        
        var = SUV(csp)

        for value in var.mutable_domain:
            # if value is consistent with assignment then
            # What is the above????
            var.value = value



    return backtrack({}, csp)