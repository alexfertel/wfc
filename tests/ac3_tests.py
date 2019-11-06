import constraint as csp
def csp_lib_test():
    p = csp.Problem()
    vardict = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    p.addVariables(vardict, ['red', 'green', 'blue'])
    
    arc_dict = [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (0, 1), (1, 2), (2, 3), (3, 4)]
    for x, y in arc_dict:
        p.addConstraint(lambda a, b: a != b, [vardict[x], vardict[y]])

    from pprint import pprint
    pprint(len(p.getSolutions()))


