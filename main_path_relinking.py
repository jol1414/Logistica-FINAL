from structure import instance, solution
from algorithms import grasp
from localsearch import  lsbestimp
import random


def copySolution(sol):
    new_sol = {}
    new_sol['instance'] = sol['instance']
    new_sol['sol'] = set(sol['sol'])
    new_sol['of'] = sol['of']
    return new_sol


def updateTop5(top5, sol):
    top5.append(copySolution(sol))
    top5.sort(key=lambda s: s['of'], reverse=True)
    if len(top5) > 5:
        top5.pop()


def pathRelinking(start, guide):
    current = copySolution(start)
    best = copySolution(start)

    while current['sol'] != guide['sol']:
        extra = current['sol'] - guide['sol']
        missing = guide['sol'] - current['sol']

        best_next = None
        best_next_of = -1

        for out_elem in extra:
            for in_elem in missing:
                cand = copySolution(current)
                cand['sol'].remove(out_elem)
                cand['sol'].add(in_elem)
                cand['of'] = solution.evaluate(cand)

                if cand['of'] > best_next_of:
                    best_next = cand
                    best_next_of = cand['of']

        current = best_next

        if current['of'] > best['of']:
            best = copySolution(current)

    return best


def executeInstance(alpha):
    path = "instances/MDG-a_2_n500_m50.txt"
    inst = instance.readInstance(path)

    top5 = []

    # generar soluciones GRASP y guardar las 5 mejores
    for _ in range(20):
        sol = grasp.execute(inst, 10, 0.0001)
        updateTop5(top5, sol)

    best = copySolution(top5[0])

    # path relinking entre pares de las 5 mejores
    for i in range(len(top5)):
        for j in range(len(top5)):
            if i != j:
                pr_sol = pathRelinking(top5[i], top5[j])
                if pr_sol['of'] > best['of']:
                    best = copySolution(pr_sol)

    # local search SOLO a la mejor solución final
    lsbestimp.improve(best)
    best['of'] = solution.evaluate(best)

    print("\nBEST SOLUTION:")
    solution.printSolution(best)

    solution.writeSolution(best, alpha)


if __name__ == '__main__':
    random.seed(2)
    for i in range(10):
        executeInstance(i / 100)