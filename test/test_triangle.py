import numpy
from helpers import _near_equal

import meshzoo


def _get_points(bary):
    corners = numpy.array(
        [[0.0, -0.5 * numpy.sqrt(3.0), +0.5 * numpy.sqrt(3.0)], [1.0, -0.5, -0.5]]
    )
    return numpy.dot(corners, bary).T


def test_triangle():
    bary, cells = meshzoo.triangle(4)
    assert len(bary.T) == 15
    assert _near_equal(numpy.sum(_get_points(bary), axis=0), [0.0, 0.0])
    assert len(cells) == 16


def test_plot2d():
    bary, cells = meshzoo.triangle(4)
    meshzoo.show2d(_get_points(bary), cells)


def test_edges():
    _, cells = meshzoo.triangle(2)
    edges_nodes, edges_cells = meshzoo.create_edges(cells)
    assert numpy.all(
        edges_nodes
        == [[0, 1], [0, 3], [1, 2], [1, 3], [1, 4], [2, 4], [3, 4], [3, 5], [4, 5]]
    )
    assert numpy.all(edges_cells == [[3, 1, 0], [5, 4, 2], [6, 3, 4], [8, 7, 6]])


if __name__ == "__main__":
    points, cells = meshzoo.triangle(5000)
    # import meshio
    # meshio.write_points_cells('triangle.vtk', points, {'triangle': cells})
