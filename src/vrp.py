#############################################################################################################
# Imports
#############################################################################################################
import GA
import numpy as np


#############################################################################################################
# Constants
#############################################################################################################
number_of_customer = 32
population_size = 50
gene_size = 16
cromossome_size = int(number_of_customer / gene_size)
generations = 10001
print_step = 1000
depot_coordinate = np.array((0, 0))
customer_coordinates = np.random.randint(-200, 200, size=(number_of_customer, 2))


#############################################################################################################
# Fitness function - distance
#############################################################################################################
def fitness(chromosome):

    # distância percorrida pelo entregador
    total = 0

    # get gene
    for i in range(len(chromosome)):

        # initialize
        routes = []

        # append depot coordinate
        routes.append(depot_coordinate)

        # get customer
        for y in range(len(chromosome[i])):

            # get customers coordinates
            customer_coordinate = customer_coordinates[chromosome[i][y]]

            # append customer coordinate
            routes.append(customer_coordinate)

        # append depot coordinate
        routes.append(depot_coordinate)

    # calc distance
    for i in range(len(routes) -1):
        total = total + GA.distance(routes[i], routes[i + 1])

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
    if epoch == 0:
        GA.plotDistances(customer_coordinates, depot_coordinate, plot)
    if epoch == (generations-1):
        GA.plotDistances(customer_coordinates, depot_coordinate, plot)


#############################################################################################################
# Main call
#############################################################################################################
if __name__ == "__main__":

    # initial population
    chromosomes = GA.populate(population_size, cromossome_size, gene_size, number_of_customer)

    # loop
    for epoch in range(0, generations):

        # log epoch
        if epoch % print_step == 0:
            print("Epoch: " + str(epoch))

        # selection by roullete
        chromosomes = GA.selectionByTournament(chromosomes, fitness)

        # apply crossover
        chromosomes = GA.crossover(chromosomes, number_of_customer)

        # apply mutation
        chromosomes = GA.mutation(chromosomes, number_of_customer)

        # print population
        if epoch % print_step == 0:
            printValues(chromosomes, epoch)
