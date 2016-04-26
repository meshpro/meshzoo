#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplistic triangular mesh on a M\"obius strip.
'''
import vtk
import mesh, mesh_io
import numpy as np
from math import pi, sin, cos
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 190
    # Number of nodes along the width of the strip (>= 2)
    nw = 30
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    #l = 5
    p = 1.5

    # seam displacement
    alpha0 = 0.0 # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning M\"obius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # How many twists are there in the "paper"?
    moebius_index = 1
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Generate suitable ranges for parametrization
    u_range = np.linspace( 0.0, 2*pi, num = nl, endpoint = False )
    v_range = np.linspace( -0.5*width, 0.5*width, num = nw )

    # Create the vertices.
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            if ( cos(alpha)>0 ):
                c =  cos(alpha)**2
            else:
                c = -cos(alpha)**2
            if ( sin(alpha)>0 ):
               s =  sin(alpha)**2
            else:
               s = -sin(alpha)**2
            nodes.append( mesh.Node( [ scale * ( r + v*c ) * cos(u),
                                       scale * ( r + v*c ) * sin(u),
                                       scale * flatness * v*s
                                     ]
                                   )
                       )

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [ i*nw + j, (i + 1)*nw + j + 1,  i     *nw + j + 1 ]
            elems.append( mesh.Cell( elem_nodes, [], vtk.VTK_TRIANGLE ) )
            elem_nodes = [ i*nw + j, (i + 1)*nw + j    , (i + 1)*nw + j + 1 ]
            elems.append( mesh.Cell( elem_nodes, [], vtk.VTK_TRIANGLE ) )
    # close the geometry
    if moebius_index % 2 == 0:
        # Close the geometry upside up (even M\"obius fold)
        for j in range(nw - 1):
            elem_nodes = [ (nl - 1)*nw + j, j + 1 , (nl - 1)*nw + j + 1 ]
            elems.append( mesh.Cell( elem_nodes, [], vtk.VTK_TRIANGLE ) )
            elem_nodes = [ (nl - 1)*nw + j, j     , j + 1  ]
            elems.append( mesh.Cell( elem_nodes, [], vtk.VTK_TRIANGLE ) )
    else:
        # Close the geometry upside down (odd M\"obius fold)
        for j in range(nw - 1):
            elem_nodes = [ (nl-1)*nw + j, (nw-1) - (j+1) , (nl-1)*nw +  j+1  ]
            elems.append( mesh.Cell( elem_nodes, [], vtk.VTK_TRIANGLE ) )
            elem_nodes = [ (nl-1)*nw + j, (nw-1) - j     , (nw-1)    - (j+1) ]
            elems.append( mesh.Cell( elem_nodes, [], vtk.VTK_TRIANGLE ) )

    # add values
    num_nodes = len( nodes )
    X = np.empty( num_nodes, dtype = complex )
    k = 0
    for u in u_range:
        for v in v_range:
            X[k] = complex( 1.0, 0.0 )
            k += 1

    # add parameters
    params = { "mu": 0.0 }

    # create the mesh data structure
    mymesh = mesh.Mesh( nodes, elems )

    # create the mesh
    mesh_io.write( "moebius_alt.e",
                   mymesh,
                   [X], ["psi"],
                   params
                 )
# ------------------------------------------------------------------------------
