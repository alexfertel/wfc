from src.csp import CSP, ac3

def map_coloring_test():
    vardict = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    variables = [i for i in range(7)]
    domains = [['red', 'green', 'blue'] for i in range(len(variables))]
    arcs = [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (0, 1), (1, 2), (2, 3), (3, 4)]
    constraints = {arc : [(x, y) for y in domains[0] for x in domains[0] if x != y] for arc in arcs}

    domains[0] = ['red']
    print(variables)
    print(domains)
    print(arcs)
    print(constraints)

    csp = CSP(variables, arcs, domains, constraints)

    ac3(csp)

    print(csp.domains)


