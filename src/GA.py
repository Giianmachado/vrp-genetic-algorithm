
#############################################################################################################
# Imports
#############################################################################################################
import numpy as np
import random
import itertools
import matplotlib.pyplot as plt
import copy


#############################################################################################################
# Random population
#############################################################################################################
def createShuffleArange(arange):
    arange = np.arange(arange)
    np.random.shuffle(arange)
    return arange


#############################################################################################################
# Random population
#############################################################################################################
def populate(population_size, chromossome_size, gene_size, number_of_customer):
    # initialize pop
    return np.array([
        np.reshape(createShuffleArange(number_of_customer),
                   (chromossome_size, gene_size))
        for i in range(population_size)
    ])


#############################################################################################################
# Euclidean Distance
#############################################################################################################
def distance(a, b):
    return np.linalg.norm(a-b)


#############################################################################################################
# Plot distances
#############################################################################################################
def plotDistances(customer_coordinates, depot_coordinate, chromosome):

    # get x and y coordinates
    x, y = customer_coordinates.T

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
            customer_coordinate = customer_coordinates[chromosome[i][y]]

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

    # get length
    length = len(chromosomes)

    # declare result
    result = []

    # define best
    best = chromosomes[0]

    # loop
    for chromosome in chromosomes:
        if fitness(chromosome) < fitness(best):
            best = chromosome
    
    # append
    result.append(best)

    # get sum of values
    for _ in range(0, length - 1):

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
def crossover(chromosomes, number_of_customer, crossover_prob, crossover_method):
    # get len
    length = len(chromosomes)

    # declare result
    result = []

    # if par
    if length % 2 == 0:
        length = int(length / 2)
    else:
        result.append(chromosomes[0])
        np.delete(chromosomes, 0)
        length = int((length - 1) / 2)

    # while len more than 1
    for _ in range(length):

        # get two random positions
        positions = random.sample(range(0, length), 2)

        # get probability
        prob = random.randint(1, 101)

        # if prob is < 90 realize crossover
        if prob < (crossover_prob * 100):

            if crossover_method == 'pmx':
                aa, bb = pmx(
                    copy.deepcopy(chromosomes[positions[0]]), copy.deepcopy(chromosomes[positions[1]]), number_of_customer
                )
            else:
                aa, bb = obx(
                    copy.deepcopy(chromosomes[positions[0]]), copy.deepcopy(chromosomes[positions[1]]), number_of_customer
                )

            # pop and append selected
            result.append(aa)
            result.append(bb)

        else:

            # pop and append selected
            result.append(chromosomes[positions[0]])
            result.append(chromosomes[positions[1]])

    # return
    return result


#############################################################################################################
# Crossover
#############################################################################################################
def obx(chromosome1, chromosome2, number_of_customer):

    # get length
    length = len(chromosome1)

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

    # calc best divisor
    if len(concatenated_chromosome2) % length != 0:
        return chromosome1, chromosome2

    # return
    return np.array(np.split(a, length)), np.array(np.split(b, length))


#############################################################################################################
# Crossover
#############################################################################################################
def pmx(chromosome1, chromosome2, number_of_customer):

    # get len
    length = len(chromosome1)

    # define number of cuts
    cuts_points_length = (length * 1) + 2

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

    # calc best divisor
    if len(concatenated_gene2) % length != 0:
        return chromosome1, chromosome2

    # return
    return np.array(np.split(a, length)), np.array(np.split(b, length))


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
def mutation(chromosomes, number_of_customer, mutation_prob, mutation_method):

    for a in range(len(chromosomes)):

        # get probability
        prob = random.randint(1, 101)

        # if prob is == 1 realize mutation
        if prob < (mutation_prob * 100):

            # get len
            length = len(chromosomes[a])

            # if operator cross
            if mutation_method == 'exchange':

                # get cut positions
                positions = random.sample(range(0, number_of_customer), 2)

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
                chromosomes[a] = np.array(
                    np.split(concatenated_chromosome, length))

            # if reverse
            else:

                # get cut positions
                positions = random.sample(range(1, number_of_customer - 1), 2)

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
                chromosomes[a] = np.array(
                    np.split(concatenated_chromosome, length))

    # return
    return chromosomes
