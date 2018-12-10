#############################################################################################################
# Imports
#############################################################################################################
import GA
import numpy as np


#############################################################################################################
# Constants
#############################################################################################################

# number of customer
number_of_customer = 16

# population size
population_size = 30

# gene size
gene_size = 4

# cromossome size
cromossome_size = int(number_of_customer / gene_size)

# number of generations
generations = 2001

# print step
print_step = 100

# depot coordinates
depot_coordinate = np.array((0, 0))

# tournament selectors
tournament_selectors = 5

# elitism probability
elitism_prob = 0.1

# crossover probability
crossover_prob = 0.95

# crossover method
# Can be obx or pmx
# default is obx
crossover_method = 'obx'

# mutation probability
mutation_prob = 0.1

# mutation method
# Can be inversion or exchange
# default is inversion
mutation_method = 'exchange'

# customer coordinates
customer_coordinates = np.array([
    [ 286,  375],    [ -19,  306],    [ 345,  372],    [ 373,  -65],
    [ 102, -395],    [ 318,  200],    [ 102, -182],    [ 164,  480],
    [-281,  -96],    [ 298,  320],    [-196, -263],    [ 107,  111],
    [  36, -266],    [-353,  236],    [ 490,  270],    [ 420,  404]
])

# generate csv file
csv_file = False

# Plot chart
plot_chart = True

# verify number of customers
if number_of_customer == 8:
    customer_coordinates = customer_coordinates[0:8]

# print all customers
print(customer_coordinates)


#############################################################################################################
# Fitness function - distance
#############################################################################################################
def fitness(chromosome):

    # distância percorrida pelo entregador
    total = 0

    # initialize
    routes = []

    # append depot coordinate
    routes.append(depot_coordinate)

    # get gene
    for i in range(len(chromosome)):

        # get customer
        for y in range(len(chromosome[i])):

            # get customers coordinates
            customer_coordinate = customer_coordinates[chromosome[i][y]]

            # append customer coordinate
            routes.append(customer_coordinate)

        # append depot coordinate
        routes.append(depot_coordinate)

    # calc distance
    for i in range(len(routes) - 1):
        total = total + \
            GA.distance(np.array(routes[i]), np.array(routes[i + 1]))

    # return value
    return total


#############################################################################################################
# Print values
#############################################################################################################
def printValues(chromosomes, epoch):
    result = []
    plot = None
    best = 0
    for chromosome in chromosomes:
        fit = fitness(chromosome)
        result.append(fit)
        if fit > best:
            best = fit
            plot = chromosome
    result = np.sort(np.array(result))

    # print result
    print(result)

    # plot chart with chromossome 0
    if plot_chart:
        if epoch == generations:
            GA.plotDistances(customer_coordinates, depot_coordinate, plot)
        if epoch == 0:
            GA.plotDistances(customer_coordinates, depot_coordinate, plot)


#############################################################################################################
# Print values on file
#############################################################################################################
def printValuesOnFile(chromosomes, file_object):
    result = []
    for chromosome in chromosomes:
        result.append(fitness(chromosome))
    result = np.sort(np.array(result))

    # print result
    file_object.write(';'.join(str(e) for e in result))
    file_object.write('\n')


#############################################################################################################
# Main call
#############################################################################################################
if __name__ == "__main__":

    # initial population
    chromosomes = GA.populate(
        population_size, cromossome_size, gene_size, number_of_customer)

    # generate file
    if csv_file:
        # file object
        file_object  = open("obx_exchange_16_4.csv", "a")

        # print first
        printValuesOnFile(chromosomes, file_object)

    # if plot chart
    if plot_chart:
        printValues(chromosomes, 0)

    # loop
    for epoch in range(0, generations):

        # log epoch
        if epoch % print_step == 0:
            print("Epoch: " + str(epoch))

        # selection by roullete
        chromosomes = GA.selectionByTournament(chromosomes, fitness, tournament_selectors, elitism_prob)

        # apply crossover
        chromosomes = GA.crossover(chromosomes, number_of_customer, crossover_prob, crossover_method)

        # apply mutation
        chromosomes = GA.mutation(chromosomes, number_of_customer, mutation_prob, mutation_method)

        # print population
        if epoch % print_step == 0:
            printValues(chromosomes, epoch + 1)

        # print on file
        if csv_file:
            # print first
            printValuesOnFile(chromosomes, file_object)

    # close file
    if csv_file:
        # close file
        file_object.close()
