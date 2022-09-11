import matplotlib.pyplot as plt
# from de import dominatingSet_Size
dominatingSet_Size  = 5000
def rank_from_population(population, child, FOOs):
    n = len(population)
    ranks = [1 for i in range(len(population))]
    evalsPOP = []

    for i in range(len(population)):
        input_vals = population[i]
        mulObj_evals = []

        for foo in FOOs:
            mulObj_evals.append(foo(input_vals))
        
        evalsPOP.append(mulObj_evals)
    
    childeval = []
    for foo in FOOs:
        childeval.append(foo(child))
    
    childrank = 1

    for i in range(n):
        # ranking child based on the parent population

        childsmall = 0
        for k in range(len(FOOs)):
            if float("{:.4f}".format(childeval[k])) < float("{:.4f}".format(evalsPOP[i][k])):
                childsmall += 1

        if childsmall == 0:
            childrank += 1
       
    return childrank
    



def rank(population, FOOs):
    n = len(population)
    ranks = [1 for i in range(len(population))]
    evalsPOP = []

    for i in range(len(population)):
        input_vals = population[i]
        mulObj_evals = []

        for foo in FOOs:
            mulObj_evals.append(foo(input_vals))
        
        evalsPOP.append(mulObj_evals)

    for i in range(n):
        for j in range(i+1, n):

            ismall = 0
            for k in range(len(FOOs)):
                if float("{:.4f}".format(evalsPOP[i][k])) < float("{:.4f}".format(evalsPOP[j][k])):
                    ismall += 1

            if ismall == len(FOOs):
                ranks[j] += 1
            elif ismall == 0:
                ranks[i] += 1
    
    return ranks

def resize_dominatingSet(dominatingSet):
    while len(dominatingSet) > dominatingSet_Size:
        dominatingSet.pop()

def update_dominatingSet(dominatingSet, population, FOOs):

    remove = set()
    add = set()

    population_ranks = rank(population, FOOs)

    oneRanks = []
    for i in range(len(population_ranks)):
        if population_ranks[i] == 1:
            oneRanks.append(population[i])

    if len(oneRanks) == 0:
        print('ALL CHILDREN ARE NON DOMINATING')

    for i in range(len(oneRanks)):
        input_vals = oneRanks[i]
        mulObj_evals = []

        for foo in FOOs:
            mulObj_evals.append(float("{:.4f}".format(foo(input_vals))))
        
        
        if len(dominatingSet) == 0:
            dominatingSet.add(tuple(mulObj_evals))

        else:
            for dominant in dominatingSet:
                evalSmall, domSmall = 0, 0

                for k in range(len(FOOs)):

                    if mulObj_evals[k] < dominant[k]:
                        evalSmall += 1
                    else:
                        domSmall += 1

                
                if evalSmall == len(FOOs):
                    add.add(tuple(mulObj_evals))
                    remove.add(dominant)

                elif evalSmall != 0:
                    add.add(tuple(mulObj_evals))
        
        
    for i in remove:
        # print(i, remove)
        dominatingSet.remove(i)
        # print("removed succesfully")
    for i in add:
        dominatingSet.add(tuple(i))
    
    resize_dominatingSet(dominatingSet)

    return dominatingSet

def plot_dominatingSet(dominatingSet):
    # only for problems with 2 objective functions

    values = list(dominatingSet)
    values.sort(key = lambda x: x[0])

    x_axis = []
    y_axis = []
    for x, y in dominatingSet:
        x_axis.append(x)
        y_axis.append(y)

    plt.scatter(x_axis, y_axis, s = 0.1)
    plt.xlabel("f1(x)")
    plt.ylabel("f2(x)")
    plt.title("Pareto Front")
    plt.show()

    

    

            