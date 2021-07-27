import numpy as np

import meshzoo


def test_cube_tetra():
    points, cells = meshzoo.cube_tetra((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 10)
    assert len(points) == 1331
    assert len(cells) == 5000

    points, cells = meshzoo.cube_tetra((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 2)
    assert len(points) == 27
    assert all(np.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 40


# def test_positive_volumes():
#     points, cells = meshzoo.cube_tetra((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 4)
#     print(meshplex.Mesh(points, cells).signed_cell_volumes)
#     assert np.all(meshplex.Mesh(points, cells).signed_cell_volumes > 0.0)


def test_cube_hexa():
    points, cells = meshzoo.cube_hexa((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 10)
    assert len(points) == 1331
    assert len(cells) == 1000
    # import meshio
    # meshio.Mesh(points, {"hexahedron": cells}).write("cube-hexa.vtk")

    points, cells = meshzoo.cube_hexa((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 2)
    assert len(points) == 27
    assert all(np.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 8
