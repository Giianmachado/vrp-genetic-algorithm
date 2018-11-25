#############################################################################################################
# Imports
#############################################################################################################
import GA
import numpy as np


#############################################################################################################
# Constants
#############################################################################################################
number_of_customer = 8
number_of_customers_by_route = 4
population_size = 5
cromossome_size = int(number_of_customer / number_of_customers_by_route)
gene_size = 3
generations = 1
print_step = 1


#############################################################################################################
# Fitness function - x^2
#############################################################################################################
def fitness(x):
    # total = 0
    # for i in range(len(x)):
    #     value = np.array(x[i]).dot(2**np.arange(np.array(x[i]).size)[::-1])
    #     total = total + (i * (value ** 4))
    # return total
    return 0


#############################################################################################################
# Main call
#############################################################################################################
if __name__ == "__main__":

    # initial population
    chromosomes = GA.populate(population_size, cromossome_size, gene_size)

    # loop
    for epoch in range(0, generations):

        # log epoch
        if epoch % print_step == 0:
            print("Epoch: " + str(epoch))

        # print population
        if epoch % print_step == 0:
            for chromosome in chromosomes:
                print(fitness(chromosome), end=" ")
            print('')

        # selection by roullete
        # chromosomes = GA.selectionByTournament(chromosomes, fitness, False)

        # apply crossover
        # chromosomes = GA.crossover(chromosomes, gene_size)

        # apply mutation
        # chromosomes = GA.mutation(chromosomes)

        # print population
        # if epoch % print_step == 0:
        #     for chromosome in chromosomes:
        #         print(fitness(chromosome), end=" ")
        #     print('')