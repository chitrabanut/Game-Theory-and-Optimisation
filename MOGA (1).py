import pygad
import numpy
num_generations = 5000
num_parents_mating = 4



sol_per_pop = 8
# num_genes = len(function_inputs)
num_genes = 1

init_range_low = -10**5
init_range_high = 10**5

parent_selection_type = "sss"
keep_parents = 1

A = 10
# gene_type=[int, float, numpy.float16, numpy.int8, numpy.float]
gene_space = [{"low" : -5, "high":10}]

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

def callback_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])


def constraint1(x, y):
    return not ((x-5)**2 + y**2 <= 25)

def constraint2(x, y):
    return not ((x-8)**2 + (y+3)**2 >= 7.7)

def checkConstraints(x, y):
    return False
    return constraint1(x, y) or constraint2(x, y)

def Obj1(solution, solution_idx):
    x = solution[0]

    if x <= 1:
        t = -1*x
    elif 1 < x <= 3:
        t = x - 2
    elif 3 < x <= 4:
        t = 4 - x
    elif x > 4:
        t = x - 4

    
    return -1*t

def Obj2(solution, solution_idx):
    x = solution[0]
    return -1*(x-5)**2

Objs = [Obj1, Obj2]
fmin = [float("inf")]*len(Objs)
fmax = [-float("inf")]*len(Objs)

# Calculating Pareto Set
Po = []
for func in Objs:
    fitness_function = func
    ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        fitness_func=fitness_function,
                        sol_per_pop=sol_per_pop,
                        num_genes=num_genes,
                        init_range_low=init_range_low,
                        init_range_high=init_range_high,
                        parent_selection_type=parent_selection_type,
                        keep_parents=keep_parents,
                        crossover_type=crossover_type,
                        mutation_type=mutation_type,
                        mutation_percent_genes=mutation_percent_genes,
                        gene_space=gene_space)

    ga_instance.run()

    var = ga_instance.best_solution()
    var = var[0]
    print(var)
    # for i in range(len(var)):
    #     var[i] *= -1

    temp = []
    for foo in Objs:
        temp.append(-1*foo(var, 0))

    Po.append(temp)

    for i in range(len(Objs)):
        fmin[i] = min(fmin[i], temp[i])
        fmax[i] = max(fmax[i], temp[i])

print(Po)
# Formulating the new Objective Function
def S(solution, solution_idx):
    temp = 1
    x = solution[0]

    for i in range(len(Objs)):
        func = Objs[i]

        t = (fmax[i] + func(solution, 0)) / (fmax[i] - fmin[i])
        temp *= t

    # if checkConstraints(x, y): return -float('inf')
    return temp

# def S(solution, solution_idx):
#     x = solution[0]

#     t = x*(x-4)*(x**2-4)/16
#     return t
# Running GA on S
ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        fitness_func=S,
                        sol_per_pop=sol_per_pop,
                        num_genes=num_genes,
                        init_range_low=init_range_low,
                        init_range_high=init_range_high,
                        parent_selection_type=parent_selection_type,
                        keep_parents=keep_parents,
                        crossover_type=crossover_type,
                        mutation_type=mutation_type,
                        mutation_percent_genes=mutation_percent_genes,
                        gene_space=gene_space)

ga_instance.run()

print(ga_instance.best_solution())


        
