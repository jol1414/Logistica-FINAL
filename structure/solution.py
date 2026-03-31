def createEmptySolution(instance):
    sol = {}
    sol['instance'] = instance
    sol['sol'] = set()
    sol['of'] = 0
    return sol


def addToSolution(sol, u, ofVariation = -1):
    if ofVariation < 0:
        for s in sol['sol']:
            sol['of'] += sol['instance']['d'][u][s]
    else:
        sol['of'] += ofVariation
    sol['sol'].add(u)


def removeFromSolution(sol, u, ofVariation = -1):
    sol['sol'].remove(u)
    if ofVariation < 0:
        for s in sol['sol']:
            sol['of'] -= sol['instance']['d'][u][s]
    else:
        sol['of'] -= ofVariation


def evaluate(sol):
    of = 0
    for s1 in sol['sol']:
        for s2 in sol['sol']:
            if s1 < s2:
                of += sol['instance']['d'][s1][s2]
    return of


def isFeasible(sol):
    return len(sol['sol']) == sol['instance']['p']


def contains(sol, u):
    return u in sol['sol']


def distanceToSol(sol, u, without = -1):
    d = 0
    for s in sol['sol']:
        if s != u and s != without:
            d += sol['instance']['d'][s][u]
    return round(d, 2)


def printSolution(sol):
    print("Solution: ", end="")
    for s in sol['sol']:
        print(s, end=" ")
    print()
    print("Objective Value: "+str(round(sol['of'], 2)))
import json
import json

import json
import os

def writeSolution(sol, alpha, filename='solutions.json'):
    """Append optimization solution to a JSON file."""
    
    # Preparar la nueva solución
    solution_list = sorted(list(sol['sol'])) if isinstance(sol['sol'], set) else sol['sol']
    new_solution = {
        'solution': solution_list,
        'objective_value': round(sol['of'], 2),
        'alpha':alpha
    }
    
    # Leer el archivo existente o crear una lista vacía
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            try:
                solutions = json.load(json_file)
                # Asegurarse de que es una lista
                if not isinstance(solutions, list):
                    solutions = [solutions]
            except json.JSONDecodeError:
                solutions = []
    else:
        solutions = []
    
    # Añadir la nueva solución
    solutions.append(new_solution)
    
    # Guardar todo el array
    with open(filename, 'w') as json_file:
        json.dump(solutions, json_file, indent=4)
    
    print(f"Solution {len(solutions)} saved to {filename}")
    print(f"Total solutions in file: {len(solutions)}")