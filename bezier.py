#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Examples for the NURBS-Python Package
    Released under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2018
"""
import os
from geomdl import BSpline
from geomdl import exchange
from geomdl import helpers
from geomdl import utilities
from geomdl.visualization import VisPlotly


# Fix file path
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Create a BSpline surface instance
surf = BSpline.Surface()

# Set degrees
surf.degree_u = 3
surf.degree_v = 3

# Set control points
#values = exchange.read_txt("ex_surface01.cpt", two_dimensional=True)

surf.set_ctrlpts(*exchange.read_txt("control_points.cpt", two_dimensional=True))

# Set knot vectors
surf.knotvector_u = utilities.generate_knot_vector(surf.degree_u, 18)
surf.knotvector_v = utilities.generate_knot_vector(surf.degree_v, 18)
print(surf.knotvector_u)
print(surf.knotvector_v)
print(len(surf.knotvector_u))
# Set evaluation delta
surf.delta = 0.25

for knot in surf.knotvector_u:
    span = helpers.find_span(surf.knotvector_u, 7, knot)
    print("Span for knot {} is =>{}".format(knot, span))
    basis = helpers.basis_function(surf.degree_u, surf.knotvector_u,span, knot)
    print ("Basis function for knot {} is {}".format(knot, basis))
# Evaluate surface points
print(surf.evaluate())

#Plot the control point grid and the evaluated surface
vis_comp = VisPlotly.VisSurface()
surf.vis = vis_comp
surf.render()

# # Good to have something here to put a breakpoint
pass