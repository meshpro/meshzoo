import numpy as np
from helpers import _get_signed_areas, _near_equal

import meshzoo


def _get_points(bary):
    corners = np.array(
        [[0.0, -0.5 * np.sqrt(3.0), +0.5 * np.sqrt(3.0)], [1.0, -0.5, -0.5]]
    )
    return np.dot(corners, bary).T


def test_triangle():
    bary, cells = meshzoo.triangle(4)
    assert len(bary.T) == 15
    assert _near_equal(np.sum(_get_points(bary), axis=0), [0.0, 0.0])
    assert len(cells) == 16

    # make sure the order of the nodes in each cell is counterclockwise
    corner_coords = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    coords = np.dot(corner_coords, bary)
    assert np.all(_get_signed_areas(coords, cells) > 0.0)


def test_plot2d():
    bary, cells = meshzoo.triangle(4)
    meshzoo.show2d(_get_points(bary), cells)


def test_edges():
    _, cells = meshzoo.triangle(2)
    edges_nodes, edges_cells = meshzoo.create_edges(cells)
    assert np.all(
        edges_nodes
        == [[0, 1], [0, 3], [1, 2], [1, 3], [1, 4], [2, 4], [3, 4], [3, 5], [4, 5]]
    )
    assert np.all(edges_cells == [[3, 1, 0], [5, 4, 2], [6, 3, 4], [8, 7, 6]])


if __name__ == "__main__":
    points, cells = meshzoo.triangle(5000)
    # import meshio
    # meshio.write_points_cells('triangle.vtk', points, {'triangle': cells})
