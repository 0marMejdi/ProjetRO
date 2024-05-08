import gurobipy as gp
from math import *

def PL2(months_number, heures_sup_cost, chaussures_fab_cost, ouvriers_lic_cost, ouvriers_rec_cost, stock_cost,
        ouvriers_dispo_cost, max_heures_supp, heures_travail_mois, heures_par_chauss, ouvriers_initial,
        stock_initial, *args):
    mois = ['mois{}'.format(i) for i in range(1, months_number + 1)]

    # Ensure the number of months matches the length of args
    if len(args) < months_number:
        raise ValueError("Insufficient demand values provided for the given number of months.")

    demandes = args[:months_number]  # Use only the first 'months_number' elements of args

    cost = [heures_sup_cost, chaussures_fab_cost, ouvriers_lic_cost, ouvriers_rec_cost, stock_cost, ouvriers_dispo_cost]
    vars = ['heures_sup', 'chaussures_fab', 'ouvriers_rec', 'ouvriers_lic', 'stock_init', 'ouvriers_dispo']
    costs = {}

    m = gp.Model('PL2')
    x = m.addVars(mois, vars, name="x", vtype=gp.GRB.INTEGER)

    for i in range(len(mois)):
        for j in range(len(vars)):
            costs[mois[i], vars[j]] = cost[j]

    m.setObjective(
        x.prod(costs)
    )

    m.addConstrs(
        x[mois[i], 'heures_sup'] <= max_heures_supp * x[mois[i], 'ouvriers_dispo']
        for i in range(len(mois))
    )
    m.addConstrs(
        x[mois[i], 'stock_init'] + x[mois[i], 'chaussures_fab'] >= demandes[i]
        for i in range(len(mois))
    )
    m.addConstrs(
        x[mois[i], 'chaussures_fab'] <= (pow(heures_par_chauss, -1)) * (
                x[mois[i], 'heures_sup'] + x[mois[i], 'ouvriers_dispo'] * heures_travail_mois)
        for i in range(len(mois))
    )

    m.addConstr(x[mois[0], 'ouvriers_dispo'] == ouvriers_initial)
    m.addConstrs(
        x[mois[i], 'ouvriers_dispo'] == x[mois[i - 1], 'ouvriers_dispo'] + x[mois[i], 'ouvriers_rec'] +
        x[mois[i], 'ouvriers_lic']
        for i in range(1, len(mois))
    )

    m.addConstr(x[mois[0], 'stock_init'] == stock_initial)
    m.addConstrs(
        x[mois[i], 'stock_init'] == x[mois[i - 1], 'stock_init'] + x[mois[i], 'chaussures_fab'] - demandes[i]
        for i in range(1, len(mois))
    )

    m.addConstrs(
        x[mois[i], vars[j]] >= 0
        for i in range(len(mois))
        for j in range(len(mois))
    )

    m.optimize()

    if m.status == gp.GRB.OPTIMAL:
        print("The problem solved to optimality.")

        solution_variables = {}
        for v in m.getVars():
            solution_variables[v.varName] = v.x

        return m.objVal, solution_variables

    elif m.status == gp.GRB.INFEASIBLE:
        print("Le modèle est infaisable.")
    elif m.status == gp.GRB.INF_OR_UNBD:
        print("Le modèle a une solution optimale infinie ou est non borné.")

    return None, None  # Return None if no optimal solution or in case of error
