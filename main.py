from structure import instance, solution
from algorithms import grasp
import random


def executeInstance(alpha):
    path = "instances/MDG-a_2_n500_m50.txt"
    inst = instance.readInstance(path)
    
    sol = grasp.execute(inst, 10, alpha)

    print("\nBEST SOLUTION:")
    solution.printSolution(sol)
    
    solution.writeSolution(sol, alpha)

if __name__ == '__main__':
    random.seed(2)
    for i in range(95):
        executeInstance(0.0001)


