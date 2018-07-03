import matplotlib as mpl
import numpy as np
from scipy.misc import comb
from geomdl import exchange
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def bernstein_poly(i, n, t):
    return comb(n, i) * (t**(n - i)) * (1 - t)**i

def reshape_into2DMatrix(points, M, N):
    return np.reshape(points, (M,N))

def get_cartesian(points):
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])
    zPoints = np.array([p[2] for p in points])

    return xPoints, yPoints, zPoints

def objective_function(xPoints, yPoints,zPoints):
    err = 0
    xvals, yvals, zvals, polynomial_array = bezier_surface(xPoints, yPoints, zPoints, nTimes = 1000)
    xvals = sum(sum(xvals))
    yvals = sum(sum(yvals))
    zvals = sum(sum(zvals))
    polynomial_array = sum(sum(polynomial_array))
    xvals = np.divide(xvals, polynomial_array)
    yvals = np.divide(yvals, polynomial_array)
    zvals = np.divide(zvals, polynomial_array)
    n = len(xPoints)
    xvals= [xp - xvals for xp in xPoints]
    yvals= [yp - xvals for yp in yPoints]
    zvals= [zp - xvals for zp in zPoints]
    print (sum(sum(np.square(xvals))))
    return err
def bezier_surface(xPoints, yPoints,zPoints, nTimes=1000):
    nPoints = len(xPoints)
    # xPoints, yPoints, zPoints = get_cartesian(points)

    t = np.linspace(0.0, 1.0, nTimes)
    polynomial_array = np.array(
        [bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)
    zvals = np.dot(zPoints, polynomial_array)

    return xvals, yvals, zvals, polynomial_array

def main():
    N = 7
    M = 7
    values = exchange.read_txt("control_points.cpt", two_dimensional=True)
    points = np.asarray(values[0])

    xPoints, yPoints, zPoints = get_cartesian(points)
    xPoints = reshape_into2DMatrix(xPoints, M, N)
    yPoints = reshape_into2DMatrix(yPoints, M, N)
    zPoints = reshape_into2DMatrix(zPoints, M, N)
    err =objective_function(xPoints,yPoints, zPoints)
    print (err)

if __name__ == "__main__":
    main()
    #nPoints = 4
    #points = np.random.rand(nPoints, 3) * 200
    #print (points)
    # xpoints = [p[0] for p in points]
    # ypoints = [p[1] for p in points]
    # zpoints = [p[2] for p in points]

    # xvals, yvals, zvals = bezier_surface(points, nTimes=1000)

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.plot(xvals, yvals, zvals, label='bezier')
    # ax.plot(xpoints, ypoints, zpoints, "ro")
    # for nr in range(len(points)):
    #     ax.text(points[nr][0], points[nr][1], points[nr][2], nr)

    #plt.show()