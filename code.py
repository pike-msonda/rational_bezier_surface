"""
    Objective Function: Minimizing the difference between two squares

    It has been applied so that, we can minimize the difference between two curves. 

"""
from utilities import Points, Bat

if __name__ == "__main__":
    point_util =  Points("bunny.pcd") #Load point data
    bat_util = Bat(10, 40)
    x, y, z = point_util.load_points()
    t = bat_util.blending_values(0, 1, 10)
    polynomials = [bat_util.bernstein_polynomial(i, len(x), t)
        for i in range(0, len(x))]
    print(len(polynomials))
    # # Initialise bat population
    # u = bat_util.intialise_population(x,y,z)
    # v = bat_util.intialise_population(x,y,z)




