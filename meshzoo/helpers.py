# -*- coding: utf-8 -*-
#
from math import copysign
import numpy


def cube(
        xmin=0.0, xmax=1.0,
        ymin=0.0, ymax=1.0,
        zmin=0.0, zmax=1.0,
        nx=11, ny=11, nz=11
        ):
    '''Canonical tetrahedrization of the cube.
    Input:
    Edge lenghts of the cube
    Number of nodes along the edges.
    '''
    # Generate suitable ranges for parametrization
    x_range = numpy.linspace(xmin, xmax, nx)
    y_range = numpy.linspace(ymin, ymax, ny)
    z_range = numpy.linspace(zmin, zmax, nz)

    # Create the vertices.
    x, y, z = numpy.meshgrid(x_range, y_range, z_range, indexing='ij')
    # We'd like to do
    # ```
    # nodes = numpy.stack([x, y, z]).T.reshape(-1, 3)
    # ```
    # but `numpy.stack` isn't available on trusty numpy for Python 3.
    nodes = numpy.vstack([x, y, z]).T.reshape(-1, 3)

    # Create the elements (cells).
    # There is 1 way to split a cube into 5 tetrahedra,
    # and 12 ways to split it into 6 tetrahedra.
    # See
    # <http://www.baumanneduard.ch/Splitting%20a%20cube%20in%20tetrahedras2.htm>
    # Also interesting: <http://en.wikipedia.org/wiki/Marching_tetrahedrons>.

    a0 = numpy.add.outer(
        numpy.array(range(nx - 1)),
        nx * numpy.array(range(ny - 1))
        )
    a = numpy.add.outer(a0, nx*ny * numpy.array(range(nz - 1)))

    # The general scheme here is:
    #  * Initialize everything with `a`, equivalent to
    #    [i + nx * j + nx*ny * k].
    #  * Add the "even" elements.
    #  * Switch the element styles for every other element to make sure the
    #    edges match at the faces of the cubes.
    # The last step requires adapting the original pattern at
    #     [1::2, 0::2, 0::2, :]
    #     [0::2, 1::2, 0::2, :]
    #     [0::2, 0::2, 1::2, :]
    #     [1::2, 1::2, 1::2, :]
    #

    # Tetrahedron 0:
    # [
    # i   + nx*j     + nx*ny * k,
    # i   + nx*(j+1) + nx*ny * k,
    # i+1 + nx*j     + nx*ny * k,
    # i   + nx*j     + nx*ny * (k+1)
    # ]
    elems0 = numpy.stack([a, a + nx, a + 1, a + nx*ny]).T

    # Every other element cube:
    # [
    # i+1 + nx * j     + nx*ny * k,
    # i+1 + nx * (j+1) + nx*ny * k,
    # i   + nx * j     + nx*ny * k,
    # i+1 + nx * j     + nx*ny * (k+1)
    # ]
    elems0[1::2, 0::2, 0::2, 0] += 1
    elems0[0::2, 1::2, 0::2, 0] += 1
    elems0[0::2, 0::2, 1::2, 0] += 1
    elems0[1::2, 1::2, 1::2, 0] += 1

    elems0[1::2, 0::2, 0::2, 1] += 1
    elems0[0::2, 1::2, 0::2, 1] += 1
    elems0[0::2, 0::2, 1::2, 1] += 1
    elems0[1::2, 1::2, 1::2, 1] += 1

    elems0[1::2, 0::2, 0::2, 2] -= 1
    elems0[0::2, 1::2, 0::2, 2] -= 1
    elems0[0::2, 0::2, 1::2, 2] -= 1
    elems0[1::2, 1::2, 1::2, 2] -= 1

    elems0[1::2, 0::2, 0::2, 3] += 1
    elems0[0::2, 1::2, 0::2, 3] += 1
    elems0[0::2, 0::2, 1::2, 3] += 1
    elems0[1::2, 1::2, 1::2, 3] += 1

    # Tetrahedron 1:
    # [
    # i   + nx*(j+1) + nx*ny * k,
    # i+1 + nx*(j+1) + nx*ny * k,
    # i+1 + nx*j     + nx*ny * k,
    # i+1 + nx*(j+1) + nx*ny * (k+1)
    # ]
    elems1 = numpy.stack([a + nx, a + 1 + nx, a + 1, a + 1 + nx + nx*ny]).T

    # Every other element cube:
    # [
    # i+1 + nx * (j+1) + nx*ny * k,
    # i   + nx * (j+1) + nx*ny * k,
    # i   + nx * j     + nx*ny * k,
    # i   + nx * (j+1) + nx*ny * (k+1)
    # ]
    elems1[1::2, 0::2, 0::2, 0] += 1
    elems1[0::2, 1::2, 0::2, 0] += 1
    elems1[0::2, 0::2, 1::2, 0] += 1
    elems1[1::2, 1::2, 1::2, 0] += 1

    elems1[1::2, 0::2, 0::2, 1] -= 1
    elems1[0::2, 1::2, 0::2, 1] -= 1
    elems1[0::2, 0::2, 1::2, 1] -= 1
    elems1[1::2, 1::2, 1::2, 1] -= 1

    elems1[1::2, 0::2, 0::2, 2] -= 1
    elems1[0::2, 1::2, 0::2, 2] -= 1
    elems1[0::2, 0::2, 1::2, 2] -= 1
    elems1[1::2, 1::2, 1::2, 2] -= 1

    elems1[1::2, 0::2, 0::2, 3] -= 1
    elems1[0::2, 1::2, 0::2, 3] -= 1
    elems1[0::2, 0::2, 1::2, 3] -= 1
    elems1[1::2, 1::2, 1::2, 3] -= 1

    # Tetrahedron 2:
    # [
    # i   + nx*(j+1) + nx*ny * k,
    # i+1 + nx*j     + nx*ny * k,
    # i   + nx*j     + nx*ny * (k+1),
    # i+1 + nx*(j+1) + nx*ny * (k+1)
    # ]
    elems2 = numpy.stack([a + nx, a + 1, a + nx*ny, a + 1 + nx + nx*ny]).T

    # Every other element cube:
    # [
    # i+1 + nx * (j+1) + nx*ny * k,
    # i   + nx * j     + nx*ny * k,
    # i+1 + nx * j     + nx*ny * (k+1),
    # i   + nx * (j+1) + nx*ny * (k+1)
    # ]
    elems2[1::2, 0::2, 0::2, 0] += 1
    elems2[0::2, 1::2, 0::2, 0] += 1
    elems2[0::2, 0::2, 1::2, 0] += 1
    elems2[1::2, 1::2, 1::2, 0] += 1

    elems2[1::2, 0::2, 0::2, 1] -= 1
    elems2[0::2, 1::2, 0::2, 1] -= 1
    elems2[0::2, 0::2, 1::2, 1] -= 1
    elems2[1::2, 1::2, 1::2, 1] -= 1

    elems2[1::2, 0::2, 0::2, 2] += 1
    elems2[0::2, 1::2, 0::2, 2] += 1
    elems2[0::2, 0::2, 1::2, 2] += 1
    elems2[1::2, 1::2, 1::2, 2] += 1

    elems2[1::2, 0::2, 0::2, 3] -= 1
    elems2[0::2, 1::2, 0::2, 3] -= 1
    elems2[0::2, 0::2, 1::2, 3] -= 1
    elems2[1::2, 1::2, 1::2, 3] -= 1

    # Tetrahedron 3:
    # [
    # i   + nx * (j+1) + nx*ny * k,
    # i   + nx * j     + nx*ny * (k+1),
    # i   + nx * (j+1) + nx*ny * (k+1),
    # i+1 + nx * (j+1) + nx*ny * (k+1)
    # ]
    elems3 = numpy.stack([
        a + nx,
        a + nx*ny,
        a + nx + nx*ny,
        a + 1 + nx + nx*ny
        ]).T

    # Every other element cube:
    # [
    # i+1 + nx * (j+1) + nx*ny * k,
    # i+1 + nx * j     + nx*ny * (k+1),
    # i+1 + nx * (j+1) + nx*ny * (k+1),
    # i   + nx * (j+1) + nx*ny * (k+1)
    # ]
    elems3[1::2, 0::2, 0::2, 0] += 1
    elems3[0::2, 1::2, 0::2, 0] += 1
    elems3[0::2, 0::2, 1::2, 0] += 1
    elems3[1::2, 1::2, 1::2, 0] += 1

    elems3[1::2, 0::2, 0::2, 1] += 1
    elems3[0::2, 1::2, 0::2, 1] += 1
    elems3[0::2, 0::2, 1::2, 1] += 1
    elems3[1::2, 1::2, 1::2, 1] += 1

    elems3[1::2, 0::2, 0::2, 2] += 1
    elems3[0::2, 1::2, 0::2, 2] += 1
    elems3[0::2, 0::2, 1::2, 2] += 1
    elems3[1::2, 1::2, 1::2, 2] += 1

    elems3[1::2, 0::2, 0::2, 3] -= 1
    elems3[0::2, 1::2, 0::2, 3] -= 1
    elems3[0::2, 0::2, 1::2, 3] -= 1
    elems3[1::2, 1::2, 1::2, 3] -= 1

    # Tetrahedron 4:
    # [
    # i+1 + nx * j     + nx*ny * k,
    # i   + nx * j     + nx*ny * (k+1),
    # i+1 + nx * (j+1) + nx*ny * (k+1),
    # i+1 + nx * j     + nx*ny * (k+1)
    # ]
    elems4 = numpy.stack([
        a + 1,
        a + nx*ny,
        a + 1 + nx + nx*ny,
        a + 1 + nx*ny
        ]).T

    # Every other element cube:
    # [
    # i   + nx * j     + nx*ny * k,
    # i+1 + nx * j     + nx*ny * (k+1),
    # i   + nx * (j+1) + nx*ny * (k+1),
    # i   + nx * j     + nx*ny * (k+1)
    # ]
    elems4[1::2, 0::2, 0::2, 0] -= 1
    elems4[0::2, 1::2, 0::2, 0] -= 1
    elems4[0::2, 0::2, 1::2, 0] -= 1
    elems4[1::2, 1::2, 1::2, 0] -= 1

    elems4[1::2, 0::2, 0::2, 1] += 1
    elems4[0::2, 1::2, 0::2, 1] += 1
    elems4[0::2, 0::2, 1::2, 1] += 1
    elems4[1::2, 1::2, 1::2, 1] += 1

    elems4[1::2, 0::2, 0::2, 2] -= 1
    elems4[0::2, 1::2, 0::2, 2] -= 1
    elems4[0::2, 0::2, 1::2, 2] -= 1
    elems4[1::2, 1::2, 1::2, 2] -= 1

    elems4[1::2, 0::2, 0::2, 3] -= 1
    elems4[0::2, 1::2, 0::2, 3] -= 1
    elems4[0::2, 0::2, 1::2, 3] -= 1
    elems4[1::2, 1::2, 1::2, 3] -= 1

    elems = numpy.vstack([
        elems0.reshape(-1, 4),
        elems1.reshape(-1, 4),
        elems2.reshape(-1, 4),
        elems3.reshape(-1, 4),
        elems4.reshape(-1, 4)
        ])

    return nodes, elems


def cylinder():
    # The width of the strip
    width = 1.0

    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 100
    # Number of nodes along the width of the strip (>= 2)
    nw = 10

    # Generate suitable ranges for parametrization
    u_range = numpy.arange(nl, dtype='d') \
        * 2 * numpy.pi \
        / nl
    v_range = numpy.arange(nw, dtype='d') \
        / (nw - 1.0)*width \
        - 0.5 * width

    # Create the vertices. This is based on the parameterization
    # of the M\'obius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    num_nodes = nl * nw
    nodes = numpy.empty(num_nodes, dtype=numpy.dtype((float, 3)))
    k = 0
    for u in u_range:
        for v in v_range:
            nodes[k] = numpy.array([numpy.cos(u), numpy.sin(u), v])
            k += 1

    # create the elements (cells)
    numelems = 2 * nl * (nw-1)
    elems = numpy.zeros([numelems, 3], dtype=int)
    k = 0
    for i in range(nl - 1):
        for j in range(nw - 1):
            elems[k] = [i*nw + j, (i + 1)*nw + j + 1,  i * nw + j + 1]
            elems[k+1] = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            k += 2

    # close the geometry
    for j in range(nw - 1):
        elems[k] = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
        elems[k+1] = [(nl - 1)*nw + j, j, j + 1]
        k += 2

    return numpy.array(nodes), numpy.array(elems)


def hexagon(ref_steps=4):
    # Circumcircle radius of the triangle.
    cc_radius = 5.0

    # Create initial nodes/elements.
    tilt = 0.0
    num_nodes = 7
    nodes = numpy.empty(num_nodes, dtype=numpy.dtype((float, 3)))
    nodes[0] = numpy.array([0.0, 0.0, 0.0])
    for k in range(6):
        phi = (tilt + k/3.0) * numpy.pi
        nodes[k+1] = cc_radius * numpy.array([
            numpy.cos(phi),
            numpy.sin(phi),
            0.0
            ])

    edges = numpy.array([
        numpy.array([0, 1]),
        numpy.array([0, 2]),
        numpy.array([0, 3]),
        numpy.array([0, 4]),
        numpy.array([0, 5]),
        numpy.array([0, 6]),
        numpy.array([1, 2]),
        numpy.array([2, 3]),
        numpy.array([3, 4]),
        numpy.array([4, 5]),
        numpy.array([5, 6]),
        numpy.array([6, 1])
        ])

    cells_nodes = numpy.array([
        numpy.array([0, 1, 2]),
        numpy.array([0, 2, 3]),
        numpy.array([0, 3, 4]),
        numpy.array([0, 4, 5]),
        numpy.array([0, 5, 6]),
        numpy.array([0, 6, 1])
        ])
    cells_edges = numpy.array([
        numpy.array([0, 6, 1]),
        numpy.array([1, 7, 2]),
        numpy.array([2, 8, 3]),
        numpy.array([3, 9, 4]),
        numpy.array([4, 10, 5]),
        numpy.array([5, 11, 0])
        ])

    # Refine.
    for k in range(ref_steps):
        nodes, edges, cells_nodes, cells_edges = \
            _refine(nodes, edges, cells_nodes, cells_edges)

    return nodes, cells_nodes


def moebius(
        moebius_index=1  # How many twists are there in the 'paper'?
        ):
    '''
    Creates a simplistic triangular mesh on a slightly Möbius strip.  The
    Möbius strip here deviates slightly from the ordinary geometry in that it
    is constructed in such a way that the two halves can be exchanged as to
    allow better comparison with the pseudo-Möbius geometry.
    '''
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 190
    # Number of nodes along the width of the strip (>= 2)
    nw = 31

    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning Möbius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip.
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=nl, endpoint=False)
    v_range = numpy.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices. This is based on the parameterization
    # of the Möbius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        # if u > pi:
        #     pre_alpha = pi / 2 * abs(u/pi - 1)**l + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * abs(u/pi - 1)**l + pi / 2
        # else:
        #     pre_alpha = pi / 2
        # if u > pi:
        #     pre_alpha = pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # else:
        #     pre_alpha = pi / 2
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            # The fundamental difference with the ordinary M'obius band here
            # are the squares.
            # It is also possible to to abs() the respective sines and cosines,
            # but this results in a non-smooth manifold.
            a = v*copysign(numpy.cos(alpha)**2, numpy.cos(alpha))
            nodes.append([
                scale * (r + a) * numpy.cos(u),
                scale * (r + a) * numpy.sin(u),
                flatness * scale * v *
                copysign(numpy.sin(alpha)**2, numpy.sin(alpha))
                ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [i*nw + j, (i + 1)*nw + j + 1,  i*nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            elems.append(elem_nodes)

    # close the geometry
    if moebius_index % 2 == 0:
        # Close the geometry upside up (even Möbius fold)
        for j in range(nw - 1):
            elem_nodes = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [(nl - 1)*nw + j, j, j + 1]
            elems.append(elem_nodes)
    else:
        # Close the geometry upside down (odd Möbius fold)
        for j in range(nw - 1):
            elem_nodes = [(nl-1)*nw + j, (nw-1) - (j+1), (nl-1)*nw + j+1]
            elems.append(elem_nodes)
            elem_nodes = [(nl-1)*nw + j, (nw-1) - j, (nw-1) - (j+1)]
            elems.append(elem_nodes)

    return numpy.array(nodes), numpy.array(elems)


def moebius2(
        moebius_index=1  # How many twists are there in the 'paper'?
        ):
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 190
    # Number of nodes along the width of the strip (>= 2)
    nw = 30

    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning Möbius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=nl, endpoint=False)
    v_range = numpy.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices.
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            if (numpy.cos(alpha) > 0):
                c = numpy.cos(alpha)**2
            else:
                c = -numpy.cos(alpha)**2
            if (numpy.sin(alpha) > 0):
                s = numpy.sin(alpha)**2
            else:
                s = -numpy.sin(alpha)**2
            nodes.append([
                scale * (r + v*c) * numpy.cos(u),
                scale * (r + v*c) * numpy.sin(u),
                scale * flatness * v*s
               ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [i*nw + j, (i + 1)*nw + j + 1,  i*nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            elems.append(elem_nodes)
    # close the geometry
    if moebius_index % 2 == 0:
        # Close the geometry upside up (even Möbius fold)
        for j in range(nw - 1):
            elem_nodes = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [(nl - 1)*nw + j, j, j + 1]
            elems.append(elem_nodes)
    else:
        # Close the geometry upside down (odd Möbius fold)
        for j in range(nw - 1):
            elem_nodes = [(nl-1)*nw + j, (nw-1) - (j+1), (nl-1)*nw + j+1]
            elems.append(elem_nodes)
            elem_nodes = [(nl-1)*nw + j, (nw-1) - j, (nw-1) - (j+1)]
            elems.append(elem_nodes)

    # create the mesh
    return numpy.array(nodes), numpy.array(elems)


def moebius3(
        nl=51,  # Number of nodes along the length of the strip
        nw=11,  # Number of nodes along the width of the strip (>= 2)
        index=1
        ):
    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning M\'obius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=nl, endpoint=False)
    v_range = numpy.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices. This is based on the parameterization
    # of the M\'obius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        # if u > pi:
        #     pre_alpha = pi / 2 * abs(u/pi -1)**l + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * abs(u/pi -1)**l + pi / 2
        # else:
        #     pre_alpha = pi / 2
        # if u > pi:
        #     pre_alpha = pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # else:
        #     pre_alpha = pi / 2
        alpha = index * pre_alpha + alpha0
        for v in v_range:
            nodes.append([
                scale * (r + v*numpy.cos(alpha)) * numpy.cos(u),
                scale * (r + v*numpy.cos(alpha)) * numpy.sin(u),
                flatness * scale * v*numpy.sin(alpha)
                ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elems.append([i*nw + j, (i + 1)*nw + j + 1,  i*nw + j + 1])
            elems.append([i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1])
    # close the geometry
    if index % 2 == 0:
        # Close the geometry upside up (even M\'obius fold)
        for j in range(nw - 1):
            elems.append([(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1])
            elems.append([(nl - 1)*nw + j, j, j + 1])
    else:
        # Close the geometry upside down (odd M\'obius fold)
        for j in range(nw - 1):
            elems.append([(nl-1)*nw + j, (nw-1) - (j+1), (nl-1)*nw + j+1])
            elems.append([(nl-1)*nw + j, (nw-1) - j, (nw-1) - (j+1)])

    return numpy.array(nodes), numpy.array(elems)


def pseudomoebius():
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 190
    # Number of nodes along the width of the strip (>= 2)
    nw = 31

    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning M\'obius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # How many twists are there in the 'paper'?
    moebius_index = 1

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=nl, endpoint=False)
    v_range = numpy.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices. This is based on the parameterization
    # of the Möbius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        # if u > pi:
        #     pre_alpha = pi / 2 * abs( u/pi -1 )**l + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * abs( u/pi -1 )**l + pi / 2
        # else:
        #     pre_alpha = pi / 2
        # if u > pi:
        #     pre_alpha = pi / 2 * ( 1 - (1-abs(u/pi-1)**p)**(1/p) ) + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * ( 1 - (1-abs(u/pi-1)**p)**(1/p) ) + pi / 2
        # else:
        #     pre_alpha = pi / 2
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            # The fundamental difference with the ordinary M'obius band here
            # are the squares.
            # It is also possible to to abs() the respective sines and cosines,
            # but this results in a non-smooth manifold.
            nodes.append([
                scale * (r - v * numpy.cos(alpha)**2) * numpy.cos(u),
                scale * (r - v * numpy.cos(alpha)**2) * numpy.sin(u),
                - flatness * scale * v * numpy.sin(alpha)**2
                ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [i*nw + j, (i + 1)*nw + j + 1,  i * nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            elems.append(elem_nodes)

    # close the geometry
    for j in range(nw - 1):
        elem_nodes = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
        elems.append(elem_nodes)
        elem_nodes = [(nl - 1)*nw + j, j, j + 1]
        elems.append(elem_nodes)

    return numpy.array(nodes), numpy.array(elems)


def rectangle(
        xmin=0.0, xmax=1.0,
        ymin=0.0, ymax=1.0,
        nx=11, ny=11,
        zigzag=True
        ):
    if zigzag:
        return _zigzag(xmin, xmax, ymin, ymax, nx, ny)
    else:
        return _canonical(xmin, xmax, ymin, ymax, nx, ny)


def _canonical(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = numpy.linspace(xmin, xmax, nx)
    y_range = numpy.linspace(ymin, ymax, ny)
    nodes = numpy.dstack(
        numpy.meshgrid(x_range, y_range, numpy.array([0.0]))
        ).reshape(-1, 3)

    # Create the elements (cells).
    # a = [i + j*nx]
    a = numpy.add.outer(
        numpy.array(range(nx - 1)),
        nx * numpy.array(range(ny - 1))
        )
    elems0 = numpy.dstack([a, a + 1, a + nx + 1]).reshape(-1, 3)
    elems1 = numpy.dstack([a, a + 1 + nx, a + nx]).reshape(-1, 3)
    elems = numpy.vstack([elems0, elems1])

    return nodes, elems


def _zigzag(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = numpy.linspace(xmin, xmax, nx)
    y_range = numpy.linspace(ymin, ymax, ny)
    nodes = numpy.dstack(
        numpy.meshgrid(x_range, y_range, numpy.array([0.0]))
        ).reshape(-1, 3)

    # Create the elements (cells).
    # a = [i + j*nx]
    a = numpy.add.outer(
        numpy.array(range(nx - 1)),
        nx * numpy.array(range(ny - 1))
        )
    elems = []
    # [i + j*nx, i+1 + j*nx, i+1 + (j+1)*nx]
    elems0 = numpy.dstack([a, a + 1, a + nx + 1])
    # [i+1 + j*nx, i+1 + (j+1)*nx, i + (j+1)*nx] for "every other" element
    elems0[0::2, 1::2, 0] += 1
    elems0[1::2, 0::2, 0] += 1
    elems0[0::2, 1::2, 1] += nx
    elems0[1::2, 0::2, 1] += nx
    elems0[0::2, 1::2, 2] -= 1
    elems0[1::2, 0::2, 2] -= 1

    # [i + j*nx, i+1 + (j+1)*nx,  i + (j+1)*nx]
    elems1 = numpy.dstack([a, a + 1 + nx, a + nx])
    # [i + j*nx, i+1 + j*nx, i + (j+1)*nx] for "every other" element
    elems1[0::2, 1::2, 1] -= nx
    elems1[1::2, 0::2, 1] -= nx

    elems = numpy.vstack([
        elems0.reshape(-1, 3), elems1.reshape(-1, 3)
        ])

    return nodes, elems


def _refine(node_coords, edges, cells_nodes, cells_edges):
    '''Canonically refine a mesh by inserting nodes at all edge midpoints
    and make four triangular elements where there was one.
    This is a very crude refinement; don't use for actual applications.
    '''
    num_nodes = len(node_coords)
    num_new_nodes = len(edges)

    # new_nodes = numpy.empty(num_new_nodes, dtype=numpy.dtype((float, 2)))
    node_coords.resize(num_nodes+num_new_nodes, 3, refcheck=False)
    # Set starting index for new nodes.
    new_node_gid = num_nodes

    # After the refinement step, all previous edge-node associations will be
    # obsolete, so record *all* the new edges.
    num_edges = len(edges)
    num_cells = len(cells_nodes)
    assert num_cells == len(cells_edges)
    num_new_edges = 2 * num_edges + 3 * num_cells
    new_edges_nodes = numpy.empty(num_new_edges, dtype=numpy.dtype((int, 2)))

    new_edge_gid = 0

    # After the refinement step, all previous cell-node associations will be
    # obsolete, so record *all* the new cells.
    num_new_cells = 4 * num_cells
    new_cells_nodes = numpy.empty(num_new_cells, dtype=numpy.dtype((int, 3)))
    new_cells_edges = numpy.empty(num_new_cells, dtype=numpy.dtype((int, 3)))
    new_cell_gid = 0

    is_edge_divided = numpy.zeros(num_edges, dtype=bool)
    edge_midpoint_gids = numpy.empty(num_edges, dtype=int)
    edge_newedges_gids = numpy.empty(num_edges, dtype=numpy.dtype((int, 2)))

    # Loop over all elements.
    for cell_id, cell in enumerate(zip(cells_edges, cells_nodes)):
        cell_edges, cell_nodes = cell
        # Divide edges.
        local_edge_midpoint_gids = numpy.empty(3, dtype=int)
        local_edge_newedges = numpy.empty(3, dtype=numpy.dtype((int, 2)))
        local_neighbor_midpoints = [[], [], []]
        local_neighbor_newedges = [[], [], []]
        for k, edge_gid in enumerate(cell_edges):
            edgenodes_gids = edges[edge_gid]
            if is_edge_divided[edge_gid]:
                # Edge is already divided. Just keep records for the cell
                # creation.
                local_edge_midpoint_gids[k] = edge_midpoint_gids[edge_gid]
                local_edge_newedges[k] = edge_newedges_gids[edge_gid]
            else:
                # Create new node at the edge midpoint.
                node_coords[new_node_gid] = \
                    0.5 * (node_coords[edgenodes_gids[0]] +
                           node_coords[edgenodes_gids[1]]
                           )
                local_edge_midpoint_gids[k] = new_node_gid
                new_node_gid += 1
                edge_midpoint_gids[edge_gid] = \
                    local_edge_midpoint_gids[k]

                # Divide edge into two.
                new_edges_nodes[new_edge_gid] = \
                    numpy.array([edgenodes_gids[0],
                                 local_edge_midpoint_gids[k]
                                 ])
                new_edge_gid += 1
                new_edges_nodes[new_edge_gid] = \
                    numpy.array([local_edge_midpoint_gids[k],
                                 edgenodes_gids[1]
                                 ])
                new_edge_gid += 1

                local_edge_newedges[k] = [new_edge_gid-2, new_edge_gid-1]
                edge_newedges_gids[edge_gid] = \
                    local_edge_newedges[k]
                # Do the household.
                is_edge_divided[edge_gid] = True
            # Keep a record of the new neighbors of the old nodes.
            # Get local node IDs.
            edgenodes_lids = [
                numpy.nonzero(cell_nodes == edgenodes_gids[0])[0][0],
                numpy.nonzero(cell_nodes == edgenodes_gids[1])[0][0]
                ]
            local_neighbor_midpoints[edgenodes_lids[0]] \
                .append(local_edge_midpoint_gids[k])
            local_neighbor_midpoints[edgenodes_lids[1]]\
                .append(local_edge_midpoint_gids[k])
            local_neighbor_newedges[edgenodes_lids[0]] \
                .append(local_edge_newedges[k][0])
            local_neighbor_newedges[edgenodes_lids[1]] \
                .append(local_edge_newedges[k][1])

        new_edge_opposite_of_local_node = numpy.empty(3, dtype=int)
        # New edges: Connect the three midpoints.
        for k in range(3):
            new_edges_nodes[new_edge_gid] = local_neighbor_midpoints[k]
            new_edge_opposite_of_local_node[k] = new_edge_gid
            new_edge_gid += 1

        # Create new elements.
        # Center cell:
        new_cells_nodes[new_cell_gid] = local_edge_midpoint_gids
        new_cells_edges[new_cell_gid] = new_edge_opposite_of_local_node
        new_cell_gid += 1
        # The three corner elements:
        for k in range(3):
            new_cells_nodes[new_cell_gid] = \
                numpy.array([cells_nodes[cell_id][k],
                             local_neighbor_midpoints[k][0],
                             local_neighbor_midpoints[k][1]
                             ])
            new_cells_edges[new_cell_gid] = \
                numpy.array([new_edge_opposite_of_local_node[k],
                             local_neighbor_newedges[k][0],
                             local_neighbor_newedges[k][1]
                             ])
            new_cell_gid += 1

    return node_coords, new_edges_nodes, new_cells_nodes, new_cells_edges


def simple_arrow():
    # create the mesh data structure
    nodes = numpy.array([
        [0.0,  0.0, 0.0],
        [2.0, -1.0, 0.0],
        [2.0,  1.0, 0.0],
        [1.0,  0.0, 0.0],
        [2.0,  0.0, 0.0]
        ])
    cells = numpy.array([
        [1, 4, 3],
        [1, 3, 0],
        [2, 3, 4],
        [0, 3, 2]
        ])
    return nodes, cells


def simple_shell():
    nodes = numpy.array([
        [+0.0,  0.0, 1.0],
        [+1.0,  0.0, 0.0],
        [+0.0,  1.0, 0.0],
        [-1.0,  0.0, 0.0],
        [+0.0, -1.0, 0.0]
        ])
    elems = numpy.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 1]
        ])

    return nodes, elems


def sphere(num_points_per_circle=20, num_circles=10, radius=1.0):
    # Mesh parameters
    n_phi = num_points_per_circle
    n_theta = num_circles

    # Generate suitable ranges for parametrization
    phi_range = numpy.linspace(0.0, 2*numpy.pi, num=n_phi, endpoint=False)
    theta_range = numpy.linspace(
            -numpy.pi/2 + numpy.pi/(n_theta-1),
            numpy.pi/2 - numpy.pi/(n_theta-1),
            num=n_theta - 2
            )

    num_nodes = len(theta_range) * len(phi_range) + 2
    nodes = numpy.empty(num_nodes, dtype=numpy.dtype((float, 3)))
    # south pole
    south_pole_index = 0
    k = 0
    nodes[k] = numpy.array([0.0, 0.0, -1.0])
    k += 1
    # nodes in the circles of latitude (except poles)
    for theta in theta_range:
        for phi in phi_range:
            nodes[k] = numpy.array([
                numpy.cos(theta) * numpy.sin(phi),
                numpy.cos(theta) * numpy.cos(phi),
                numpy.sin(theta)
                ])
            k += 1
    # north pole
    north_pole_index = k
    nodes[k] = numpy.array([0.0, 0.0, 1.0])

    nodes *= radius

    # create the elements (cells)
    num_elems = 2 * (n_theta-2) * n_phi
    elems = numpy.empty(num_elems, dtype=numpy.dtype((int, 3)))
    k = 0

    # connections to south pole
    for i in range(n_phi - 1):
        elems[k] = numpy.array([south_pole_index, i+1, i+2])
        k += 1
    # close geometry
    elems[k] = numpy.array([south_pole_index, n_phi, 1])
    k += 1

    # non-pole elements
    for i in range(n_theta - 3):
        for j in range(n_phi - 1):
            elems[k] = numpy.array([
                i*n_phi + j+1,
                i*n_phi + j+2,
                (i+1)*n_phi + j+2
                ])
            k += 1
            elems[k] = numpy.array([
                i*n_phi + j+1,
                (i+1)*n_phi + j+2,
                (i+1)*n_phi + j + 1
                ])
            k += 1

    # close the geometry
    for i in range(n_theta - 3):
        elems[k] = numpy.array([(i+1)*n_phi, i*n_phi + 1, (i+1)*n_phi + 1])
        k += 1
        elems[k] = numpy.array([(i+1)*n_phi, (i+1)*n_phi + 1, (i+2)*n_phi])
        k += 1

    # connections to the north pole
    for i in range(n_phi - 1):
        elems[k] = numpy.array([
            i+1 + n_phi*(n_theta-3) + 1,
            i + n_phi*(n_theta-3) + 1,
            north_pole_index
            ])
        k += 1
    # close geometry
    elems[k] = numpy.array([
        0 + n_phi*(n_theta-3) + 1,
        n_phi-1 + n_phi*(n_theta-3) + 1,
        north_pole_index
        ])
    k += 1
    assert k == num_elems, 'Wrong element count.'

    return nodes, elems


def triangle(ref_steps=2):

    # Circumcircle radius of the triangle.
    cc_radius = 5.0

    # Create initial nodes/elements.
    nodes = cc_radius * numpy.array([
        numpy.array([0.0, 1.0, 0.0]),
        numpy.array([-0.5*numpy.sqrt(3.0), -0.5, 0.0]),
        numpy.array([0.5*numpy.sqrt(3.0), -0.5, 0.0])
        ])
    edges = numpy.array([
        numpy.array([0, 1]),
        numpy.array([0, 2]),
        numpy.array([1, 2])
        ])
    cells_nodes = numpy.array([[0, 1, 2]], dtype=int)
    cells_edges = numpy.array([[0, 1, 2]], dtype=int)

    # Refine.
    for _ in range(ref_steps):
        nodes, edges, cells_nodes, cells_edges = \
            _refine(nodes, edges, cells_nodes, cells_edges)

    return nodes, cells_nodes


def tube(length=5.0, radius=1.0, n=30):
    # Number of nodes along the width of the strip (>= 2)
    # Choose it such that we have approximately square boxes.
    nw = int(round(length * n/(2*numpy.pi*radius)))

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=n, endpoint=False)
    v_range = numpy.linspace(-0.5*length, 0.5*length, num=nw)

    # Create the vertices.
    nodes = []
    for u in u_range:
        x = radius * numpy.cos(u)
        y = radius * numpy.sin(u)
        for v in v_range:
            nodes.append(numpy.array([x, y, v]))

    # create the elements (cells)
    elems = []
    for i in range(n - 1):
        for j in range(nw - 1):
            elems.append([i*nw + j, (i + 1)*nw + j + 1, i * nw + j + 1])
            elems.append([i*nw + j, (i + 1)*nw + j,     (i + 1)*nw + j + 1])
    # close the geometry
    for j in range(nw - 1):
        elems.append([(n - 1)*nw + j, j + 1, (n - 1)*nw + j + 1])
        elems.append([(n - 1)*nw + j, j, j + 1])

    return numpy.array(nodes), numpy.array(elems)
