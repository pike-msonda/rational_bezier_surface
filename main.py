import random
import pcl
import os
from BatAlgorithm import BatAlgorithm
import matplotlib as mpl
import numpy as np
from scipy.misc import comb
from geomdl import exchange
  


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]

def create_control_points(M, N, points):
    count = 0
    #ctrlpts = []
    with open("control_points.cpt", 'w') as file:
        for row in chunks(points, M):
            data = ";".join(map(str, row))
            points = data.replace("[", "")
            control = points.replace("]", "")
            if count < N:
                # for r in row:
                #     ctrlpts.append(tuple(list(r)))
                file.write(control)
                file.write('\n')
                count += 1
    #return ctrlpts

def bernstein_poly(i, n, t):
    return comb(n, i) * (t**(n - i)) * (1 - t)**i

def reshape_into2DMatrix(points, M, N):
    return np.reshape(points, (M,N))

def get_cartesian(points):
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])
    zPoints = np.array([p[2] for p in points])

    return xPoints, yPoints, zPoints

def objective_function(xPoints, yPoints,zPoints, nTimes):
    xvals, yvals, zvals, polynomial_array = bezier_surface(xPoints, yPoints, zPoints, nTimes = nTimes)
    xvals = sum(sum(xvals))
    yvals = sum(sum(yvals))
    zvals = sum(sum(zvals))
    polynomial_array = sum(sum(polynomial_array))
    xvals = np.divide(xvals, polynomial_array)
    yvals = np.divide(yvals, polynomial_array)
    zvals = np.divide(zvals, polynomial_array)
    xvals= [xp - xvals for xp in xPoints]
    yvals= [yp - xvals for yp in yPoints]
    zvals= [zp - xvals for zp in zPoints]
    xerr = (sum(sum(np.square(xvals))))
    yerr = (sum(sum(np.square(yvals))))
    zerr = (sum(sum(np.square(zvals))))
    return xerr, yerr, zerr

def bezier_surface(xPoints, yPoints,zPoints, nTimes=500):
    nPoints = len(xPoints)
    # xPoints, yPoints, zPoints = get_cartesian(points)

    t = np.linspace(0.0, 1.0, nTimes)
    polynomial_array = np.array(
        [bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)
    zvals = np.dot(zPoints, polynomial_array)

    return xvals, yvals, zvals, polynomial_array

cloud = pcl.load("bunny.pcd")
def Fun(D, sol):
    val = 0.0
    N = D
    M = D 
    point_cloud = cloud.to_list()
    create_control_points(M,N, point_cloud)
    values = exchange.read_txt("control_points.cpt", two_dimensional=True)
    points = np.asarray(values[0])

    xPoints, yPoints, zPoints = get_cartesian(points)
    xPoints = reshape_into2DMatrix(xPoints, M, N)
    yPoints = reshape_into2DMatrix(yPoints, M, N)
    zPoints = reshape_into2DMatrix(zPoints, M, N)
    xerr, yerr, zerr =objective_function(xPoints,yPoints, zPoints,nTimes=M*N)
    val = sum([xerr, zerr, yerr])
    # print ("x error: {}".format(xerr))
    # print ("y error: {}".format(yerr))
    # print ("z error: {}".format(zerr))
    return val

print ("Initialising Bat algorithm")
for i in range(1, 19):
    Algorithm = BatAlgorithm(D=i, NP=6, N_Gen=10, A=0.5, r=0.5, Qmin=0.0,
            Qmax=2.0, Lower=-1.0, Upper= 1.0, function=Fun)
    Algorithm.move_bat()