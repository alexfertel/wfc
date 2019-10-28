from src.csp import CSP, ac3, Variable, Arc

def map_coloring_test():
    vardict = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    vars = []
    for index, item in enumerate(vardict):
        vars.append(Variable(item, index, ['red', 'green', 'blue']))

    arc_dict = [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (0, 1), (1, 2), (2, 3), (3, 4)]
    arcs = []
    for i, j in arc_dict:
        arcs.append(Arc(vars[i], vars[j], [(x, y) for y in vars[i].domain for x in vars[j].domain if x != y]))
        arcs.append(Arc(vars[j], vars[i], [(x, y) for y in vars[i].domain for x in vars[j].domain if x != y]))

    # constraints = {arc : [(x, y) for y in domains[0] for x in domains[0] if x != y] for arc in arcs}

    # domains[0] = ['red']
    print(vars)
    # print(domains)
    print(arcs)
    # print(constraints)

    csp = CSP(vars, arcs)

    ac3(csp)



