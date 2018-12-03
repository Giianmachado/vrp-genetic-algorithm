
#############################################################################################################
# Imports
#############################################################################################################
import numpy as np
import random
import itertools
import matplotlib.pyplot as plt


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
def selectionByTournament(chromosomes, fitness):

    # get length
    length = len(chromosomes)

    # declare result
    result = []

    # get sum of values
    for _ in range(0, length):

        # get random positions
        positions = random.sample(range(0, length), 3)

        # define gene to compare
        compare = chromosomes[positions[0]]

        # loop
        for position in positions:
            if fitness(chromosomes[position]) < fitness(compare):
                compare = chromosomes[position]

        # append selected
        result.append(compare)

    # # return
    return result


#############################################################################################################
# Crossover
#############################################################################################################
def crossover(chromosomes, number_of_customer):
    # get len
    length = len(chromosomes)

    # declare result
    result = []

    # while len more than 1
    while length > 0:

        # get two random positions
        if length > 1:
            positions = random.sample(range(0, length), 2)
        else:
            result.append(chromosomes[0])
            break

        # get probability
        prob = random.randint(1, 101)

        # if prob is < 90 realize crossover
        if prob < 90:

            # set cross values
            chromosomes[positions[0]], chromosomes[positions[1]] = crossValues(
                chromosomes[positions[0]], chromosomes[positions[1]
                                                       ], number_of_customer
            )

        # pop and append selected
        result.append(chromosomes[positions[0]])
        result.append(chromosomes[positions[1]])

        # pop values
        chromosomes = [i for j, i in enumerate(
            chromosomes) if j not in positions]

        # get len
        length = len(chromosomes)

    # return
    return result


#############################################################################################################
# Crossover
#############################################################################################################
def crossValues(chromosome1, chromosome2, number_of_customer):

    # get length
    length = len(chromosome1)

    # get cut point
    positions = random.sample(range(0, number_of_customer), 3)

    # concat values
    concatenated_chromosome1 = np.array(list(itertools.chain.from_iterable(chromosome1)))
    concatenated_chromosome2 = np.array(list(itertools.chain.from_iterable(chromosome2)))

    # sort positions
    positions.sort()

    # change gene 1
    a = reorder(np.copy(concatenated_chromosome1), np.copy(concatenated_chromosome2), positions)
    
    # change gene 1
    b = reorder(np.copy(concatenated_chromosome2), np.copy(concatenated_chromosome1), positions)

    # calc best divisor
    if len(concatenated_chromosome2) % length != 0:
        return chromosome1, chromosome2
        
    # return
    return np.array(np.split(a, length)), np.array(np.split(b, length))


#############################################################################################################
# Reorder array
#############################################################################################################
def reorder(a, b, p):
    # new positions
    p2 = np.array([0, 0, 0])

    # get indexes from another array
    for i in range(len(p)):
        p2[i] = list(b).index(a[p[i]])

    # sort indexes
    p2.sort()

    # change values by index
    for i in range(len(p)):
        a[p[i]] = b[p2[i]]

    # return 
    return a


#############################################################################################################
# Mutation
#############################################################################################################
def mutation(chromosomes, number_of_customer):

    for a in range(len(chromosomes)):

        # get probability
        prob = random.randint(1, 101)

        # if prob is == 1 realize mutation
        if prob < 6:

            # get len
            length = len(chromosomes[a])

            # get cut positions
            positions = random.sample(range(1, number_of_customer-1), 2)

            # sort postions
            positions.sort()

            # concatenate
            concatenated_chromosome = np.array(list(itertools.chain.from_iterable(chromosomes[a])))

            # get and reverse range
            reversed_interval = np.copy(concatenated_chromosome)[positions[0]:(positions[1] + 1)]

            # reverse values
            reversed_interval, = np.fliplr([reversed_interval])

            # set reversed interval
            concatenated_chromosome[positions[0]:(positions[1] + 1)] = reversed_interval

            # set new value
            chromosomes[a] = np.array(np.split(concatenated_chromosome, length))

    # return
    return chromosomes
