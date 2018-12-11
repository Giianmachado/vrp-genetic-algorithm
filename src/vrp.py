#############################################################################################################
# Imports
#############################################################################################################
import GA
import dataset
import numpy as np


#############################################################################################################
# Constants
#############################################################################################################

# dataset name
# dataset_file = './datasets/A-n32-k5.vrp'
# dataset_file = './datasets/A-n53-k7.vrp'
# dataset_file = './datasets/P-n16-k8.vrp'
dataset_file = './datasets/P-n19-k2.vrp'

# population size
population_size = 50

# number of generations
generations = 1001

# print step
print_step = 10

# tournament selectors
tournament_selectors = 5

# elitism probability
elitism_prob = 0.2

# crossover probability
crossover_prob = 1

# crossover method
# Can be obx or pmx
# default is obx
crossover_method = 'obx'

# mutation probability
mutation_prob = 0.4

# mutation method
# Can be inversion or exchange
# default is inversion
mutation_method = 'exchange'

# generate csv file
csv_file = False

# Plot chart
plot_chart = True

# get capacity
capacity = dataset.getCapacity(dataset_file)

# number of customer
number_of_customers = dataset.getnumberOfCustomers(dataset_file)

# get customer coordinates
customers = dataset.getCustomers(dataset_file, number_of_customers)

# depot coordinates
depot_coordinate = customers[0].get_position()

# remove depot from customers
customers = customers[1:(number_of_customers)]


#############################################################################################################
# Fitness function - distance
#############################################################################################################
def fitness(chromosome):

    # total value of fitness
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
            customer_coordinate = customers[chromosome[i][y] - 1].get_position()

            # append customer coordinate
            routes.append(customer_coordinate)

        # append depot coordinate
        routes.append(depot_coordinate)

        # calc distance
        for i in range(len(routes) - 1):
            total = total + GA.distance(np.array(routes[i]), np.array(routes[i + 1]))

    # return value
    return total


#############################################################################################################
# Print values
#############################################################################################################
def printValues(chromosomes, epoch):
    result = []
    plot = chromosomes[0]
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
            GA.plotDistances(customers, depot_coordinate, plot)
        if epoch == 0:
            GA.plotDistances(customers, depot_coordinate, plot)


#############################################################################################################
# Main call
#############################################################################################################
if __name__ == "__main__":
    
    # print header
    print('##########################################################')
    print('INFORMATION')
    print('##########################################################')
    print('')

    # log info
    print('dataset_file: ' + str(dataset_file))
    print('population_size: ' + str(population_size))
    print('generations: ' + str(generations))
    print('print_step: ' + str(print_step))
    print('tournament_selectors: ' + str(tournament_selectors))
    print('elitism_prob: ' + str(elitism_prob))
    print('crossover_prob: ' + str(crossover_prob))
    print('crossover_method: ' + str(crossover_method))
    print('mutation_prob: ' + str(mutation_prob))
    print('mutation_method: ' + str(mutation_method))
    print('csv_file: ' + str(csv_file))
    print('plot_chart: ' + str(plot_chart))
    print('capacity: ' + str(capacity))
    print('number_of_customers: ' + str(number_of_customers))
    print('depot_coordinate: ' + str(depot_coordinate))

    # print header
    print('')
    print('##########################################################')
    print('CUSTOMERS')
    print('##########################################################')
    print('')

    # loop
    for customer in customers:
        print(str(customer.get_customer_id()) + ': ' + str(customer.get_position()) + '\tdemand: ' + str(customer.get_demand()))

    print('')
    print('##########################################################')
    print('END LOG')
    print('##########################################################')
    print('')

    # # initial population
    chromosomes = GA.populate(population_size, capacity, customers)

    # if plot chart
    print('Initial fitness')
    printValues(chromosomes, 0)

    # loop
    for epoch in range(0, generations):

        # log epoch
        if epoch % print_step == 0:
            print("Epoch: " + str(epoch))

        # selection by roullete
        chromosomes = GA.selectionByTournament(chromosomes, fitness, tournament_selectors, elitism_prob)

        # # apply crossover
        chromosomes = GA.crossover(chromosomes, crossover_prob, crossover_method, capacity, customers, elitism_prob, fitness)

        # apply mutation
        chromosomes = GA.mutation(chromosomes, mutation_prob, mutation_method, capacity, customers, elitism_prob, fitness)

        # print population
        if epoch % print_step == 0:
            printValues(chromosomes, epoch + 1)
