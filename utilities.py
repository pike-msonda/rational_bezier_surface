"""
    Contains a set of utility functions

"""
import pcl
import numpy as np
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

    def objective_function(self, function):
        fx = function(self.dimension)
        return fx

class RationalBezierSurface:

    def __init__ (self, u, v):
        self.u = u
        self.v = v

    def bernstein_polynomial(self, i, n, t):
         return comb(n, i) * (t**(n - i)) * (1 - t)**i



    