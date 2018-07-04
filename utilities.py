"""
    Contains a set of utility functions

"""
import pcl
import numpy as np
from random import sample
from scipy.misc import comb

class Points:

    def __init__(self,point_file):
        self.point_file = point_file
    
    def load_points(self, type="pcd"):
        """
            Return point information as x,y,z
            params:
                type: <string> 
        """
        points = ""
        if type == "pcd":
            points = self.pcl_load(self.point_file)

        return self.split_points(points)

    def split_points(self, points):
        """
            Separates point data into x, y, z 
            params:
                points: <list>
        """ 
        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])
        z = np.array([p[2] for p in points])

        return x, y, z

    def pcl_load(self, filename):
        cloud = pcl.load(self.point_file)
        points = cloud.to_list()
        return points



class Bat:

    def __init__(self, dimension, population_size):
        self.dimension = dimension
        self.population_size = population_size

    def intialise_population(self, x, y, z):
        """
            Initialise the bat population. 
            params
                x: <ndarray>
                y: <ndarray>
                z: <ndarray>
        """
        pop_x = []
        pop_y = []
        pop_z = []
        print ("Creating a {} population of dimension {}".format(
            self.population_size, self.dimension))
        for i in range (self.population_size):
            pop_x.append(sample(list(x), self.dimension))
            pop_y.append(sample(list(y), self.dimension))
            pop_z.append(sample(list(z), self.dimension))
        return (pop_x,pop_y, pop_z)

    def intialise_weights(self):
        """
            Create random weights
        """
        return np.random.uniform(-1, 0, size =self.dimension)

    def objective_function(self, u, v):
        
        return 

class RationalBezierSurface:
    def bernstein_polynomial(self, i, n, t):
         return comb(n, i) * (t**(n - i)) * (1 - t)**i



    