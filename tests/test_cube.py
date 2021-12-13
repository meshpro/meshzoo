import numpy as np

import meshzoo

from .helpers import signed_simplex_volumes


def test_positive_volumes():
    x_range = np.linspace(0.0, 1.0, 5)
    y_range = np.linspace(0.0, 1.0, 5)
    z_range = np.linspace(0.0, 1.0, 5)
    points, cells = meshzoo.cube_tetra(x_range, y_range, z_range)
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_cube_tetra():
    x_range = np.linspace(0.0, 1.0, 11)
    y_range = np.linspace(0.0, 1.0, 11)
    z_range = np.linspace(0.0, 1.0, 11)
    points, cells = meshzoo.cube_tetra(x_range, y_range, z_range)
    assert len(points) == 1331
    assert len(cells) == 5000


def test_cube_tetra2():
    x_range = np.linspace(0.0, 1.0, 3)
    y_range = np.linspace(0.0, 1.0, 3)
    z_range = np.linspace(0.0, 1.0, 3)
    points, cells = meshzoo.cube_tetra(x_range, y_range, z_range)
    assert len(points) == 27
    assert all(np.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 40


def test_cube_tetra3():
    x_range = [0.0, 1.0]
    y_range = [0.0, 0.5, 1.0]
    z_range = [0.0, 0.3, 0.7, 1.0]
    points, cells = meshzoo.cube_tetra(x_range, y_range, z_range)

    assert len(points) == 24
    assert all(np.sum(points, axis=0) == [12.0, 12.0, 12.0])
    assert cells.tolist() == [
        [0, 1, 2, 6],
        [12, 13, 14, 18],
        [8, 9, 10, 14],
        [1, 3, 2, 9],
        [13, 15, 14, 21],
        [9, 11, 10, 17],
        [1, 2, 6, 9],
        [13, 14, 18, 21],
        [9, 10, 14, 17],
        [1, 6, 7, 9],
        [13, 18, 19, 21],
        [9, 14, 15, 17],
        [2, 6, 9, 8],
        [14, 18, 21, 20],
        [10, 14, 17, 16],
        [12, 13, 6, 14],
        [8, 9, 2, 10],
        [20, 21, 14, 22],
        [13, 15, 9, 14],
        [9, 11, 5, 10],
        [21, 23, 17, 22],
        [13, 14, 9, 6],
        [9, 10, 5, 2],
        [21, 22, 17, 14],
        [13, 6, 9, 7],
        [9, 2, 5, 3],
        [21, 14, 17, 15],
        [14, 6, 8, 9],
        [10, 2, 4, 5],
        [22, 14, 16, 17],
    ]


def test_cube_hexa():
    x_range = np.linspace(0.0, 1.0, 11)
    y_range = np.linspace(0.0, 1.0, 11)
    z_range = np.linspace(0.0, 1.0, 11)
    points, cells = meshzoo.cube_hexa(x_range, y_range, z_range)
    assert len(points) == 1331
    assert len(cells) == 1000
    # import meshio
    # meshio.Mesh(points, {"hexahedron": cells}).write("cube-hexa.vtk")


def test_cube_hexa2():
    x_range = np.linspace(0.0, 1.0, 3)
    y_range = np.linspace(0.0, 1.0, 3)
    z_range = np.linspace(0.0, 1.0, 3)
    points, cells = meshzoo.cube_hexa(x_range, y_range, z_range)
    assert len(points) == 27
    assert all(np.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 8


def test_cube_hexa3():
    x_range = [0.0, 1.0]
    y_range = [0.0, 0.5, 1.0]
    z_range = [0.0, 0.3, 0.7, 1.0]
    points, cells = meshzoo.cube_hexa(x_range, y_range, z_range)

    assert len(points) == 24
    assert all(np.sum(points, axis=0) == [12.0, 12.0, 12.0])
    assert cells.tolist() == [
        [0, 1, 3, 2, 6, 7, 9, 8],
        [6, 7, 9, 8, 12, 13, 15, 14],
        [12, 13, 15, 14, 18, 19, 21, 20],
        [2, 3, 5, 4, 8, 9, 11, 10],
        [8, 9, 11, 10, 14, 15, 17, 16],
        [14, 15, 17, 16, 20, 21, 23, 22],
    ]
