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
