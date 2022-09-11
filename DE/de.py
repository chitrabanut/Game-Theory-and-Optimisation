#------------------------------------------------------------------------------+
#
#   Nathan A. Rooy
#   A simple, bare bones, implementation of differential evolution with Python
#   August, 2017
#
#------------------------------------------------------------------------------+

#--- IMPORT DEPENDENCIES ------------------------------------------------------+

import random
from xml import dom
import utils
from utils import update_dominatingSet, rank_from_population, rank, plot_dominatingSet
import sample_functions
#--- EXAMPLE COST FUNCTIONS ---------------------------------------------------+

# def func1(x):
#     # Sphere function, use any bounds, f(0,...,0)=0
#     return x[0]**2

# def func2(x):
#     # Beale's function, use bounds=[(-4.5, 4.5),(-4.5, 4.5)], f(3,0.5)=0.
#     return (x[0]-2)**2

def func1(x):
    x = x[0]

    if x <= 1:
        return -x
    elif 1 < x <= 3:
        return x-2
    elif 3 < x <= 4:
        return 4-x
    elif x > 4:
        return x-4

def func2(x):
    return (x[0]-5)**2

#--- FUNCTIONS ----------------------------------------------------------------+


def ensure_bounds(vec, bounds):

    vec_new = []
    # cycle through each variable in vector 
    for i in range(len(vec)):

        # variable exceedes the minimum boundary
        if vec[i] < bounds[i][0]:
            vec_new.append(bounds[i][0])

        # variable exceedes the maximum boundary
        if vec[i] > bounds[i][1]:
            vec_new.append(bounds[i][1])

        # the variable is fine
        if bounds[i][0] <= vec[i] <= bounds[i][1]:
            vec_new.append(vec[i])
        
    return vec_new


#--- MAIN ---------------------------------------------------------------------+

def main(FOOs, bounds, popsize, mutate, recombination, maxiter):

    #--- INITIALIZE A POPULATION (step #1) ----------------+
    dominatingSet = set() # dominating set
    population = []
    for i in range(0,popsize):
        indv = []
        for j in range(len(bounds)):
            indv.append(random.uniform(bounds[j][0],bounds[j][1]))
        population.append(indv)
    
    offspringPop = [0 for i in range(popsize)]
            
    #--- SOLVE --------------------------------------------+

    # cycle through each generation (step #2)
    for i in range(1,maxiter+1):
        print('GENERATION:',i, "||", len(dominatingSet))

        gen_scores = [] # score keeping

        # cycle through each individual in the population
        for j in range(0, popsize):

            #--- MUTATION (step #3.A) ---------------------+
            
            # select three random vector index positions [0, popsize), not including current vector (j)
            canidates = list(range(0,popsize))
            canidates.remove(j)
            random_index = random.sample(canidates, 3)

            x_1 = population[random_index[0]]
            x_2 = population[random_index[1]]
            x_3 = population[random_index[2]]
            x_t = population[j]     # target individual

            # subtract x3 from x2, and create a new vector (x_diff)
            x_diff = [x_2_i - x_3_i for x_2_i, x_3_i in zip(x_2, x_3)]

            # multiply x_diff by the mutation factor (F) and add to x_1
            v_donor = [x_1_i + mutate * x_diff_i for x_1_i, x_diff_i in zip(x_1, x_diff)]
            v_donor = ensure_bounds(v_donor, bounds)

            #--- RECOMBINATION (step #3.B) ----------------+

            v_trial = []
            for k in range(len(x_t)):
                crossover = random.random()
                if crossover <= recombination:
                    v_trial.append(v_donor[k])

                else:
                    v_trial.append(x_t[k])
            
            offspringPop[j] = v_trial # populating the offspring population. (size of offspringPOP == size of population) 
                    
        #--- GREEDY SELECTION (step #3.C) -------------+
        # Greedy selection will be performed on the basis of rank

        # getting parents ranks
        par_rank = rank(population, FOOs)
        # off_rank = rank(offspringPop, FOOs)

        for index in range(len(offspringPop)):

            
            child_rank = rank_from_population(population, offspringPop[index], FOOs)

            if child_rank <= par_rank[index]:
                population[index] = offspringPop[index]

        
        #--- Updating dominating set (step #3.D) -------------+
        dominatingSet = update_dominatingSet(dominatingSet, offspringPop, FOOs)

        # score_trial  = cost_func(v_trial)
        # score_target = cost_func(x_t)

        # if score_trial < score_target:
        #     population[j] = v_trial
        #     gen_scores.append(score_trial)
        #     print('   >',score_trial, v_trial)

        # else:
        #     print( '   >',score_target, x_t)
        #     gen_scores.append(score_target)

        
        
        
        #--- SCORE KEEPING --------------------------------+

        # gen_avg = sum(gen_scores) / popsize                         # current generation avg. fitness
        # gen_best = min(gen_scores)                                  # fitness of best individual
        # gen_sol = population[gen_scores.index(min(gen_scores))]     # solution of best individual

        # print( '      > GENERATION AVERAGE:',gen_avg)
        # print( '      > GENERATION BEST:',gen_best)
        # print( '         > BEST SOLUTION:',gen_sol,'\n')

    return dominatingSet

#--- CONSTANTS ----------------------------------------------------------------+

cost_func = sample_functions.FOO1                  # Cost function
bounds = sample_functions.bounds1            # Bounds [(x1_min, x1_max), (x2_min, x2_max),...]
popsize = 50                        # Population size, must be >= 4
mutate = 0.7                        # Mutation factor [0,2]
recombination = 0.7                 # Recombination rate [0,1]
maxiter = 2000                        # Max number of generations (maxiter)

dominatingSet_Size = 5000

#--- RUN ----------------------------------------------------------------------+

dominatingSet = main(cost_func, bounds, popsize, mutate, recombination, maxiter)
# print(dominatingSet)
utils.plot_dominatingSet(dominatingSet)

#--- END ----------------------------------------------------------------------+