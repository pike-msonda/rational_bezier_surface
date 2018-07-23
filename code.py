"""
    Objective Function: Minimizing the difference between two squares

    It has been applied so that, we can minimize the difference between two curves. 

"""
from utilities import Points, Bat

if __name__ == "__main__":
    point_util =  Points("bunny.pcd") #Load point data
    bat_util = Bat(4, 40, 16, 4)
    points = point_util.load_points()
    t = bat_util.blending_values(0, 1, 10)
    bats = bat_util.intialise_population(points)
    poly = bat_util.bernstein_polynomial(0, 0 ,t)
    fx, fy, fz = bat_util.objective_function(bats)
    print(list(zip(fx,fy,fz)))
    # # Initialise bat population




