# -*- coding: utf-8 -*-
#
import numpy


# pylint: disable=too-many-arguments
def rectangle(
        xmin=0.0, xmax=1.0,
        ymin=0.0, ymax=1.0,
        nx=11, ny=11,
        zigzag=True
        ):
    if zigzag:
        return _zigzag(xmin, xmax, ymin, ymax, nx, ny)

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
