
#############################################################################################################
# Imports
#############################################################################################################
import numpy as np
from customer import Customer


#############################################################################################################
# Get capacity from dataset file
#############################################################################################################
def getCapacity(filename):
    # open file
    lines = tuple(open(filename, 'r'))

    # loop lines
    for line in lines:

        try:

            # verify line
            line.index("CAPACITY")

            # return depot coordinates
            return int(line.split(':', 1)[1])

        except ValueError:
            continue

    # return capacity
    print('capacity not found')
    exit(0)


#############################################################################################################
# Get number of customers from dataset file
#############################################################################################################
def getnumberOfCustomers(filename):
    # open file
    lines = tuple(open(filename, 'r'))

    # loop lines
    for line in lines:

        try:

            # verify line
            line.index("DIMENSION")

            # return depot coordinates
            return int(line.split(':', 1)[1])

        except ValueError:
            continue

    # return capacity
    print('number of customer (DIMENSION) not found')
    exit(0)


#############################################################################################################
# Get depot coordinate from dataset file
#############################################################################################################
def getDepotCoordinate(filename):

    # open file
    lines = tuple(open(filename, 'r'))

    # loop lines
    for i, line in enumerate(lines):

        try:

            # verify line
            line.index("DEPOT_SECTION")

            # return depot coordinates
            return np.array([int(lines[i+1]), int(lines[i+2])])

        except ValueError:
            continue

    # return capacity
    print('depot coordinate not found')
    exit(0)


#############################################################################################################
# Get customers positions from dataset file
#############################################################################################################
def getCustomers(filename, number_of_customers):

    # open file
    lines = tuple(open(filename, 'r'))

    # declare result
    result = np.array([])

    # loop lines
    for i, line in enumerate(lines):

        try:

            # verify line
            line.index("NODE_COORD_SECTION")

            # return depot coordinates
            for j in range(number_of_customers):

                # split value
                values = lines[i + 1 + j].split(' ', 2)

                # get customer_id
                customer = Customer(int(values[0]), int(values[1]), int(values[2]), 0)

                # append customer
                result = np.append(result, customer)

            # return depot coordinates
            for customer in result:

                # split value
                values = lines[i + number_of_customers + 1 + customer.get_customer_id()].split(' ', 2)

                # verify validate
                if int(values[0]) == int(customer.get_customer_id()):
                    customer.set_demand(int(values[1]))

            return result

        except ValueError:
            continue

    # return capacity
    print('node coord not found')
    exit(0)
