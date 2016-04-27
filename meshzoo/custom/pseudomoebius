#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplistic triangular mesh on a M\"obius strip.
'''
import vtk
import mesh, mesh_io
import numpy as np
from math import pi, sin, cos
# ==============================================================================
def _main():

    # get the file name to be written to
    file_name = _parse_options()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 190
    # Number of nodes along the width of the strip (>= 2)
    nw = 31
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

    # Create the vertices. This is based on the parameterization
    # of the M\"obius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        #if u > pi:
            #pre_alpha = pi / 2 * abs( u/pi -1 )**l + pi / 2
        #elif u < pi:
            #pre_alpha = - pi / 2 * abs( u/pi -1 )**l + pi / 2
        #else:
            #pre_alpha = pi / 2
        #if u > pi:
            #pre_alpha = pi / 2 * ( 1 - (1-abs(u/pi-1)**p)**(1/p) ) + pi / 2
        #elif u < pi:
            #pre_alpha = - pi / 2 * ( 1 - (1-abs(u/pi-1)**p)**(1/p) ) + pi / 2
        #else:
            #pre_alpha = pi / 2
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            # The fundamental difference with the ordinary M"obius band here are
            # the squares.
            # It is also possible to to abs() the respective sines and cosines,
            # but this results in a non-smooth manifold.
            nodes.append( mesh.Node( [ scale * ( r - v*cos(alpha)**2 ) * cos(u),
                                       scale * ( r - v*cos(alpha)**2 ) * sin(u),
                                       - flatness * scale * v*sin(alpha)**2
                                     ]
                                   )
                       )

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [ i*nw + j, (i + 1)*nw + j + 1,  i     *nw + j + 1 ]
            elems.append( mesh.Cell( elem_nodes,
                                     [], # edges
                                     [], # faces
                                     vtk.VTK_TRIANGLE
                                   )
                        )
            elem_nodes = [ i*nw + j, (i + 1)*nw + j    , (i + 1)*nw + j + 1 ]
            elems.append( mesh.Cell( elem_nodes,
                                     [], # edges
                                     [], # faces
                                     vtk.VTK_TRIANGLE
                                   )
                        )
    # close the geometry
    for j in range(nw - 1):
        elem_nodes = [ (nl - 1)*nw + j, j + 1 , (nl - 1)*nw + j + 1 ]
        elems.append( mesh.Cell( elem_nodes,
                                  [], # edges
                                  [], # faces
                                  vtk.VTK_TRIANGLE
                                )
                    )
        elem_nodes = [ (nl - 1)*nw + j, j     , j + 1  ]
        elems.append( mesh.Cell( elem_nodes,
                                  [], # edges
                                  [], # faces
                                  vtk.VTK_TRIANGLE
                                )
                    )

    # add values
    num_nodes = len( nodes )
    X = np.empty( num_nodes, dtype = complex )
    k = 0
    for u in u_range:
        for v in v_range:
            X[k] = complex( 1.0, 0.0 )
            k += 1

    # Add thickness values in such a way as to increase
    # the thickness towards the boundaries.
    thickness = np.empty( num_nodes, dtype = float )
    alpha = 1.0    # thickness at the center of the tube
    beta  = 1024.0 # thickness at the boundary
    p     = 8      # steepness of the thickness function towards the boundary
    t = (beta-alpha) / (0.5*width)**p
    k  = 0
    for u in u_range:
        for v in v_range:
            thickness[k] = alpha + t * abs(v)**p
            k += 1

    # Add magnetic vector potential corresponding to
    # B = ( 0, 1, 0 ).
    import magnetic_vector_potentials
    A = np.empty( (num_nodes,3), dtype = float )
    k = 0
    for u in u_range:
        for v in v_range:
            A[k,:] = magnetic_vector_potentials.mvp_z( nodes[k].coords )
            k += 1

    # add parameters
    params = { "mu": 0.0 }

    # create the mesh data structure
    mymesh = mesh.Mesh( nodes, elems )

    # create the mesh
    mesh_io.write_mesh( file_name,
                        mymesh,
                        [X,A,thickness], ["psi","A","thickness"],
                        params
                       )
    return
# ==============================================================================
def _parse_options():
    '''Parse input options.'''
    import optparse, sys

    usage = "usage: %prog outfile"

    parser = optparse.OptionParser( usage = usage )

    (options, args) = parser.parse_args()

    if not args  or  len(args) != 1:
        parser.print_help()
        sys.exit( "\nProvide a file to be written to." )

    return args[0]
# ==============================================================================
if __name__ == "__main__":
    _main()
# ==============================================================================
