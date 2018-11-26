#############################################################################################################
# Imports
#############################################################################################################
import GA
import numpy as np


#############################################################################################################
# Constants
#############################################################################################################
number_of_customer = 8
population_size = 5
gene_size = 4
cromossome_size = int(number_of_customer / gene_size)
generations = 1
print_step = 1
depot_coordinate = np.array((0, 0))
customer_coordinates = np.random.randint(-20, 20, size=(number_of_customer, 2))

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
# Main call
#############################################################################################################
if __name__ == "__main__":

    # initial population
    chromosomes = GA.populate(population_size, cromossome_size, gene_size, number_of_customer)

    # plot chart with chromossome 0
    GA.plotDistances(customer_coordinates, depot_coordinate, chromosomes[0])

    # test fitness
    print(fitness(chromosomes[0]))

    # # loop
    # for epoch in range(0, generations):

    #     # log epoch
    #     if epoch % print_step == 0:
    #         print("Epoch: " + str(epoch))

    #     # print population
    #     if epoch % print_step == 0:
    #         for chromosome in chromosomes:
    #             print(fitness(chromosome), end=" ")
    #         print('')

    #     # selection by roullete
    #     # chromosomes = GA.selectionByTournament(chromosomes, fitness, False)

    #     # apply crossover
    #     # chromosomes = GA.crossover(chromosomes, gene_size)

    #     # apply mutation
    #     # chromosomes = GA.mutation(chromosomes)

    #     # print population
    #     # if epoch % print_step == 0:
    #     #     for chromosome in chromosomes:
    #     #         print(fitness(chromosome), end=" ")
    #     #     print('')