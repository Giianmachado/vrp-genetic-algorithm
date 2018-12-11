#############################################################################################################
# Imports
#############################################################################################################
import numpy as np


#############################################################################################################
# create customer class
#############################################################################################################
class Customer:

    # constructor
    def __init__(self, customer_id, x, y, demand):
        self.customer_id = customer_id
        self.x = x
        self.y = y
        self.demand = demand

    def get_customer_id(self):
        return self.customer_id
   
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_demand(self):
        return self.demand

    def get_position(self):
        return np.array([self.get_x(), self.get_y()])

    def set_demand(self, demand):
        self.demand = demand