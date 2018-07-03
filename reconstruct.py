import pcl
import os
import numpy as np
from geomdl import BSpline
from geomdl import exchange
from geomdl import utilities, helpers
from geomdl.visualization import VisPlotly


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]

def create_control_points(M, N, points):
    count = 0
    ctrlpts = []
    with open("control_points.cpt", 'w') as file:
        for row in chunks(points, M):
            data = ";".join(map(str, row))
            points = data.replace("[", "")
            control = points.replace("]", "")
            if count < N:
                for r in row:
                    ctrlpts.append(tuple(list(r)))
                file.write(control)
                file.write('\n')
                count += 1
    return ctrlpts
def main():
    M = 7
    N = 7
    #Load PC data, 
    cloud = pcl.load("bunny.pcd")
    points = cloud.to_list()
    # Fix file path
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Create a BSpline surface instance
    surf = BSpline.Surface()

    # Set degrees
    surf.degree_u = 3
    surf.degree_v = 3

    surf.set_ctrlpts(*exchange.read_txt("control_points.cpt", two_dimensional=True))

    surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, 7)
    surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, 7)
    print(surf.knotvector_u)
    print(surf.knotvector_v)
    print(len(surf.knotvector_u))
    # Set evaluation delta
    surf.delta = 0.25
    basis_functions = []
    for knot in surf.knotvector_u:
        span = helpers.find_span(surf.knotvector_u, 7, knot)
        print("Span for knot {} is =>{}".format(knot, span))
        basis = helpers.basis_function(surf.degree_u, surf.knotvector_u,span, knot)
        basis_functions.append(basis)
        print ("Basis function for knot {} is {}".format(knot, basis))

    #print (points)
    control_points =create_control_points(M,N, points)
    
    basis_res = []
    for b in range(len(basis_functions)):
        basis_res.append(np.tensordot(basis_functions[b], basis_functions[b], axes=1))
   
    new_points = []
    for n in range(N*M):  
        for b in range(len(basis_res)):
            new_points.append(tuple(float(basis_res[b]) * c for c in control_points[n]))

    x =0
    y = 0
    z = 0
    for n in range(len(new_points)):
        x += new_points[n][0]
        y += new_points[n][1]
        z += new_points[n][2]

    sums = [x, y, z]
    for p in points:
        print([a - b for a, b in zip(p, sums)])

#generate control points 
if __name__ == "__main__":
     main()
     