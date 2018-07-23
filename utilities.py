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
            points = self.pcl_load()
        return points

    def split_points(self, points):
        """
            Separates point data into x, y, z 
            params:
                points: <list>
        """ 
        print(points)
        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])
        z = np.array([p[2] for p in points])

        return x, y, z

    def pcl_load(self):
        cloud = pcl.load(self.point_file)
        points = cloud.to_list()
        return points



class Bat:

    def __init__(self, order, population_size, u, v):
        self.order = order
        self.population_size = population_size
        self.u = u
        self.v = v
        self.num_control_points = np.power(order, 2)

    def intialise_population(self,points):
        """
            Initialise the bat population. 
            params
                x: <ndarray>
                y: <ndarray>
                z: <ndarray>
        """
        population = []
        print ("Creating {} bat populations".format(self.population_size))

        for i in range (self.population_size):
            print("Creating population {}".format(i))
            population.append(sample(points, self.u*self.v))
        
        return population

    def intialise_weights(self):
        """
            Create random weights
        """
        return np.random.uniform(-1, 0, size =(self.u, self.v))

    def form_column_vector(self, surface, n, m):
        return np.reshape(surface, (m,n))

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

    def objective_function(self,bats):
        """
            Objective function: Minimum of two squares
            params:
                u: <tuple>
                v: <tuple>
        """
        weights = self.intialise_weights()
        blending_constant = max([self.u, self.v])
        t =  self.blending_values(0,1, blending_constant)
        xnum, ynum, znum = [],[],[]
        xden, yden, zden = [],[],[]
        rx, ry, rz = [],[],[]
        err_x, err_y, err_z = [],[],[]
        point = []
        for b in range(0, self.population_size):
            x, y, z = self.split_points(bats[b])
            x = self.form_column_vector(np.array(x), self.v, self.u)
            y = self.form_column_vector(np.array(y), self.v, self.u)
            z = self.form_column_vector(np.array(z), self.v, self.u)
            for i in range(0, self.u):
                for j  in range(0, self.v):
                    point.append((x[i][j], y[i][j], z[i][j]))
                    u_polynomial =  self.bernstein_polynomial(i,self.u,t)
                    v_polynomial =  self.bernstein_polynomial(j,self.v,t)
                    xnum.append(sum(np.multiply(weights[i][j], np.multiply(x[i][j],
                        np.multiply(u_polynomial, v_polynomial)))))
                    ynum.append(sum(np.multiply(weights[i][j], np.multiply(y[i][j],
                        np.multiply(u_polynomial, v_polynomial)))))
                    znum.append(sum(np.multiply(weights[i][j], np.multiply(z[i][j],
                        np.multiply(u_polynomial, v_polynomial)))))
                    xden.append(sum(np.multiply(weights[i][j],
                        np.multiply(u_polynomial, v_polynomial))))
                    yden.append(sum(np.multiply(weights[i][j],
                        np.multiply(u_polynomial, v_polynomial))))
                    zden.append(sum(np.multiply(weights[i][j],
                        np.multiply(u_polynomial, v_polynomial))))

            xref = np.divide(sum(xnum), sum(xden))
            yref = np.divide(np.sum(ynum), sum(yden))
            zref = np.divide(sum(znum), sum(zden))
            for p in point:
                rx.append(np.power(p[0], 2) - np.power(xref, 2))
                ry.append(np.power(p[1], 2) - np.power(yref, 2))
                rz.append(np.power(p[2], 2) - np.power(zref, 2))
            err_x.append(sum(rx))
            err_y.append(sum(ry))
            err_z.append(sum(rz))
            rx,ry,rz, point= [],[],[], []
            
        return err_x, err_y, err_z

    def bernstein_polynomial(self, i, n, t):
        """
            Bernstein Polynomial function
            params:
                i: <int> order
                n: <int> degree
                t: <int> 
        """

        return comb(n, i) * (t**(n - i)) * (1 - t)**i

    def blending_values(self, min, max, nTimes):
        return np.linspace(min, max, nTimes)