import meshplex
import numpy as np

import meshzoo


def test_ball_hexa():
    points, cells = meshzoo.ball_hexa(11)
    # import meshio
    # meshio.Mesh(points, {"hexahedron": cells}).write("ball-hexa.vtk")
    assert len(points) == 1331
    assert len(cells) == 1000


def test_ball_tetra():
    points, cells = meshzoo.ball_tetra(11)
    # import meshio
    # meshio.Mesh(points, {"tetra": cells}).write("ball-tetra.vtk")
    assert len(points) == 1331
    assert len(cells) == 5000


def test_positive_volumes():
    points, cells = meshzoo.ball_tetra(3)
    print(meshplex.Mesh(points, cells).signed_cell_volumes)
    assert np.all(meshplex.Mesh(points, cells).signed_cell_volumes > 0.0)
