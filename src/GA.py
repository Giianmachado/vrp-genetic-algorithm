
#############################################################################################################
# Imports
#############################################################################################################
import numpy as np
import random
import itertools
import matplotlib.pyplot as plt
import copy
import math


#############################################################################################################
# shuffle arange
#############################################################################################################
def createShuffleArange(arange):

    # create array
    arange = np.arange(arange)

    # shuffle values
    np.random.shuffle(arange)

    # return
    return arange


#############################################################################################################
# Random population
#############################################################################################################
def populate(population_size, capacity, customers):

    # initialize
    chromosomes = np.array([
        createShuffleArange(len(customers))
        for i in range(population_size)
    ])

    # get new chromossomes
    chromosomes = separateByCapacity(chromosomes, capacity, customers)

    # return
    return chromosomes


#############################################################################################################
# Separate routes based on capacity
#############################################################################################################
def separateByCapacity(chromosomes, capacity, customers):

    # define result
    result = []

    # calc gene
    for chromosome in chromosomes:

        # declare new chromossome
        new_chromosome = []

        # declare gene
        gene = []

        # total
        total = 0

        # loop
        for index in chromosome:

            # get demand
            demand = customers[index].get_demand()

            # while total < capacity
            if (total + demand) > capacity:

                # append new gene
                new_chromosome.append(gene.copy())

                # total = 0
                total = 0

                # delete gene
                del gene[:]

            # sum value
            total = total + demand

            # append gene
            gene.append(index)

        # append new gene
        new_chromosome.append(gene.copy())

        # set new chromossome
        result.append(new_chromosome)

    # return
    return result


#############################################################################################################
# Euclidean Distance
#############################################################################################################
def distance(a, b):
    return np.linalg.norm(a-b)


#############################################################################################################
# Plot distances
#############################################################################################################
def plotDistances(customers, depot_coordinate, chromosome):

    # get x and y coordinates
    x = [customer.get_x() for customer in customers]
    y = [customer.get_y() for customer in customers]

    # get x and y depot coordinates
    x_depot, y_depot = depot_coordinate.T

    # scatter x and y
    plt.scatter(x, y, color='b')

    # scatter x_depot and y_depot
    plt.scatter(x_depot, y_depot, color='r')

    # define grid properties
    plt.grid(color='grey', linestyle='-', linewidth=0.1)

    # connect customers
    # get individual
    for i in range(len(chromosome)):

        # initialize
        x_connect = np.array([])
        y_connect = np.array([])

        # append depot
        x_connect = np.append(x_connect, x_depot)
        y_connect = np.append(y_connect, y_depot)

        # get gene
        for y in range(len(chromosome[i])):

            # get customers coordinates
            customer_coordinate = customers[chromosome[i]
                                            [y] - 1].get_position()

            # append values
            x_connect = np.append(x_connect, customer_coordinate[0])
            y_connect = np.append(y_connect, customer_coordinate[1])

        # append depot
        x_connect = np.append(x_connect, x_depot)
        y_connect = np.append(y_connect, y_depot)

        # random color function
        def r(): return random.randint(0, 255)

        # set connections
        plt.plot(x_connect, y_connect, color='#%02X%02X%02X' % (r(), r(), r()))

    # show
    return plt.show()


#############################################################################################################
# Select by Tournament
#############################################################################################################
def selectionByTournament(chromosomes, fitness, tournament_selectors, elitism):

    # declare result
    result = []

    # apply elitism
    while len(result) < math.floor(elitism * len(chromosomes)) + 1:
        best = chromosomes[0]
        pos = 0
        for i in range(len(chromosomes)):
            if fitness(chromosomes[i]) < fitness(best):
                pos = i
                best = chromosomes[i]
        result.append(best.copy())
        chromosomes = np.delete(chromosomes, [pos], axis=0)

    # get length
    length = len(chromosomes)

    # get sum of values
    for _ in range(0, length):

        # get random positions
        positions = random.sample(range(0, length), tournament_selectors)

        # define gene to compare
        compare = chromosomes[positions[0]]

        # loop
        for position in positions:
            if fitness(chromosomes[position]) < fitness(compare):
                compare = chromosomes[position]

        # append selected
        result.append(compare)

    # # return
    return np.array(result)


#############################################################################################################
# Crossover
#############################################################################################################
def crossover(chromosomes, crossover_prob, crossover_method, capacity, customers, elitism, fitness):

    # declare result
    result = []

    # create copy of chromossomes
    chromosomes_copy = chromosomes.copy()

    # apply elitism
    while len(result) < math.floor(elitism * len(chromosomes)) + 1:
        best = chromosomes[0]
        pos = 0
        for i in range(len(chromosomes)):
            if fitness(chromosomes[i]) < fitness(best):
                pos = i
                best = chromosomes[i]
        result.append(
            np.array(list(itertools.chain.from_iterable(best.copy()))))
        chromosomes = np.delete(chromosomes, [pos], axis=0)

    # get length
    length = len(chromosomes)

    # if par
    if length % 2 == 0:
        length = int(length / 2)
    else:
        result.append(
            np.array(list(itertools.chain.from_iterable(chromosomes[0]))))
        np.delete(chromosomes, 0)
        length = int((length - 1) / 2)

    # while len more than 1
    for _ in range(length):

        # get two random positions
        positions = random.sample(range(0, len(chromosomes_copy)), 2)

        # make obx
        if crossover_method == 'pmx':
            aa, bb = pmx(
                copy.deepcopy(chromosomes_copy[positions[0]]), copy.deepcopy(
                    chromosomes_copy[positions[1]]), len(customers)
            )
        else:
            aa, bb = obx(
                copy.deepcopy(chromosomes_copy[positions[0]]), copy.deepcopy(
                    chromosomes_copy[positions[1]]), len(customers)
            )

        # append selected
        result.append(aa.copy())
        result.append(bb.copy())

    # return
    return separateByCapacity(result, capacity, customers)


#############################################################################################################
# Crossover
#############################################################################################################
def obx(chromosome1, chromosome2, number_of_customer):

    # get cut point
    positions = random.sample(range(0, number_of_customer), 3)

    # concat values
    concatenated_chromosome1 = np.array(
        list(itertools.chain.from_iterable(chromosome1)))
    concatenated_chromosome2 = np.array(
        list(itertools.chain.from_iterable(chromosome2)))

    # sort positions
    positions.sort()

    # change gene 1
    a = reorder(np.copy(concatenated_chromosome1),
                np.copy(concatenated_chromosome2), positions)

    # change gene 1
    b = reorder(np.copy(concatenated_chromosome2),
                np.copy(concatenated_chromosome1), positions)

    # return
    return np.array(a), np.array(b)


#############################################################################################################
# Crossover
#############################################################################################################
def pmx(chromosome1, chromosome2, number_of_customer):

    # get len
    length = len(chromosome1)

    # define number of cuts
    cuts_points_length = 3

    # get gene_size
    gene_size = int(number_of_customer / length)

    # get cut point
    cuts_points = random.sample(
        range(1, length * gene_size - 1), cuts_points_length
    )
    cuts_points.append(0)
    cuts_points.append(length * gene_size)
    cuts_points.sort()

    # concat values
    concatenated_gene1 = np.array(
        list(itertools.chain.from_iterable(chromosome1)))
    concatenated_gene2 = np.array(
        list(itertools.chain.from_iterable(chromosome2)))

    # first child
    a = changePosition(np.copy(concatenated_gene1),
                       np.copy(concatenated_gene2), cuts_points)

    # second child
    b = changePosition(np.copy(concatenated_gene2),
                       np.copy(concatenated_gene1), cuts_points)

    # return
    return np.array(a), np.array(b)


#############################################################################################################
# Change on positions
#############################################################################################################
def changePosition(a, b, p):

    # loop
    for i in range(len(p) - 1):

        # cut gene 1
        if i % 2 == 0:

            # loop
            for j in range(p[i], p[i + 1]):

                # get pos
                pos = list(a).index(b[j])

                # # change a with value b
                a[pos] = a[j]

                # and other replace
                a[j] = b[j]

    # return
    return a


#############################################################################################################
# Reorder array
#############################################################################################################
def reorder(a, b, p):
    # new positions
    p2 = np.array(np.zeros(len(p)))

    # get indexes from another array
    for i in range(len(p)):
        p2[i] = list(b).index(a[p[i]])

    # sort indexes
    p2.sort()

    # change values by index
    for i in range(len(p)):
        # print(p2[i])
        a[p[i]] = b[int(p2[i])]

    # return
    return a


#############################################################################################################
# Mutation
#############################################################################################################
def mutation(chromosomes, mutation_prob, mutation_method, capacity, customers, elitism, fitness):

    # declare result
    result = []

    # apply elitism
    while len(result) < math.floor(elitism * len(chromosomes)) + 1:
        best = chromosomes[0]
        pos = 0
        for i in range(len(chromosomes)):
            if fitness(chromosomes[i]) < fitness(best):
                pos = i
                best = chromosomes[i]
        result.append(
            np.array(list(itertools.chain.from_iterable(best.copy()))))
        chromosomes = np.delete(chromosomes, [pos], axis=0)

    # get length
    length = len(chromosomes)

    # loop
    for a in range(length):

        # get probability
        prob = random.randint(1, 101)

        # if prob is == 1 realize mutation
        if prob < (mutation_prob * 100):

            # if operator cross
            if mutation_method == 'exchange':

                # get cut positions
                positions = random.sample(range(0, len(customers)), 2)

                # sort postions
                positions.sort()

                # concatenate
                concatenated_chromosome = np.array(
                    list(itertools.chain.from_iterable(chromosomes[a])))

                # get and reverse range
                aux = np.copy(concatenated_chromosome)[positions[0]]

                # set reversed interval
                concatenated_chromosome[positions[0]
                                        ] = concatenated_chromosome[positions[1]]

                # set seconda value
                concatenated_chromosome[positions[1]] = aux

                # set new value
                result.append(concatenated_chromosome)

            # if reverse
            else:

                # get cut positions
                positions = random.sample(range(1, len(customers) - 1), 2)

                # sort postions
                positions.sort()

                # concatenate
                concatenated_chromosome = np.array(
                    list(itertools.chain.from_iterable(chromosomes[a])))

                # get and reverse range
                aux = np.copy(concatenated_chromosome)[
                    positions[0]:(positions[1] + 1)]

                # set seconda value
                concatenated_chromosome[positions[0]:(
                    positions[1] + 1)], = np.fliplr([aux])

                # set new value
                result.append(concatenated_chromosome)
        else:

            # append
            result.append(
                np.array(list(itertools.chain.from_iterable(chromosomes[a]))))

    # return
    return separateByCapacity(result, capacity, customers)
