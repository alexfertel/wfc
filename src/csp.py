def ac3(csp):
    q = list(csp.arcs)

    if q:
        (i, j) = q.pop()
        
        if revise(csp, (i, j)):
            if not csp.domains[i]: return False

            for k in [k for (l, k) in csp.arcs if l == i and k != j]:
                q.append((k, i))
    
    return True

def revise(csp, (i, j)):
    revised = False
    for x in cps.domains[i]:
        # TODO
        # if no value y in D j allows (x ,y) to satisfy the constraint between X i and X j then
        csp.domains[i].remove(x)
        revised = True

    return revised
