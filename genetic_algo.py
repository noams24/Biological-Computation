import numpy as np
from random import randint, uniform
from matrix import Matrix

BOUNDING_BOX_AREA = 9
GAME_OF_LIFE_MAX_ITERATION = 1000
MAT_SIZE = 50
CELL_CIZE = 8

POPULATION_SIZE = 10
PROBABILITY_OF_LIVE = 0.3
MUTATION_PROBABILITY = 0.5
MAX_GENERATIONS = 20
MAX_GENERATIONS_WITHOUT_IMPROVEMENT = 5

STATS_FITNESS_MIN = []
STATS_FITNESS_MAX = []
STATS_FITNESS_AVG = []


'''
create_random_population: creates random population, calculates fitness, generations of each solution and put them
                            into a list that sorted by fitness
                        Returns
                            > a list of [chromosome,fitness,generations]
'''

def create_random_population():
    population = []
    for i in range(POPULATION_SIZE):
        chromosome = np.random.choice(a=[1, 0], size=(BOUNDING_BOX_AREA),
                                      p=[PROBABILITY_OF_LIVE, 1 - PROBABILITY_OF_LIVE])
        fitness_tuple = calculate_fitness(
            chromosome)  # calculates the fitness of each chromosome, and number of generations as a tuple
        fitness = fitness_tuple[0]
        generations = fitness_tuple[1]
        population.append([list(chromosome), fitness, generations])
    population.sort(key=lambda x: x[1])
    return population


'''
calculate_fitness: runs game of life of a given chromosome and returns it's fitness
    Input
        > 'chromosome' a list that contains 0,1.
    Returns
        > fitness, generations (both type is integer)
'''

def calculate_fitness(chromosome):
    mat = Matrix(MAT_SIZE, chromosome)
    mat_history = []
    mat_history.append(mat.cells)

    for i in range(GAME_OF_LIFE_MAX_ITERATION):
        mat.change_mat()
        if len(mat_history) > 3:
            if mat.cells in mat_history:
                return mat.calculate_area(), i #can also use mat.sum_cells()
            mat_history.pop(0)
        mat_history.append(mat.cells)
    return 0, 0


'''
roulette_wheel_selection: a genetic operator used for selecting potentially useful solution for recombination.
                          given an list of solutions, choose one.
    Input
        > 'population': list of chromosomes
        > 'total_fitness": sum of the their total fitness
    Returns
        > a list that contains the chromosome
'''

def roulette_wheel_selection(population, total_fitness):
    n = uniform(0, total_fitness)
    for i in range(0, POPULATION_SIZE):
        if n < population[i][1]:
            return population[i][0]
        n -= population[i][1]
    return population[0][0]


'''
crossover: a genetic operator used to combine the genetic information of two parents to generate new offspring
           given two parents, creates a new solution that combines two of the parents evenly.
    Input
        > 'parent1', 'parent2': lists that represent chromosome of 0 and 1
    Returns
        > list that contains the new chromosome
'''
def crossover(parent1, parent2):
    child = []
    for i in range(BOUNDING_BOX_AREA):
        rand = randint(0, 1)
        if rand:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child


'''
mutation: a genetic operator used to maintain genetic diversity from one generation to another.
          given a chromosome, change every bit in probability of 'MUTATION_PROBABILITY'
    Input
        > 'child': list that represent chromosome of 0 and 1
    Output
        > list that contains the new chromosome
'''

def mutation(child):
    for i in range(len(child)):
        rand = randint(0, 100) / 100
        if rand < MUTATION_PROBABILITY:
            child[i] = 1 - child[i]  # change 0 to 1 and 1 to 0
    return child


'''
next_generation: given a list of population of chromosomes, creates new population with genetic algorithm
    Input
        > 'population': list of chromosomes
    Output
        > the new population
'''

def next_generation(population):
    total_fitness = 0
    for item in population:
        total_fitness += item[1]

    STATS_FITNESS_MIN.append(population[0][1])
    STATS_FITNESS_MAX.append(population[-1][1])
    STATS_FITNESS_AVG.append(round(total_fitness / POPULATION_SIZE))

    new_population = []

    for i in range(POPULATION_SIZE):  # iterate as population size
        # selection: Parent Selection
        parent1 = roulette_wheel_selection(population, total_fitness)
        parent2 = roulette_wheel_selection(population, total_fitness)

        # crossover:
        child = crossover(parent1, parent2)

        # mutation:
        child = mutation(child)
        fitness_tuple = calculate_fitness(child)
        fitness = fitness_tuple[0]
        generation = fitness_tuple[1]
        new_population.append([child, fitness, generation])

    new_population.sort(key=lambda x: x[1])
    return new_population
