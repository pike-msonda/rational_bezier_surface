"""
    Objective Function: Minimizing the difference between two squares

    It has been applied so that, we can minimize the difference between two curves. 

"""
from utilities import Points, RationalBezierSurface, Bat

if __name__ == "__main__":
    point_util =  Points("bunny.pcd") #Load point data
    x, y, z = point_util.load_points()
    bat_util = Bat(10, 40)
    u=bat_util.intialise_population(x, y,z)
    print (u[3])



