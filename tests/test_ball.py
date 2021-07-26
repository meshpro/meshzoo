import numpy as np
from helpers import _get_signed_volumes_tetra

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

    volumes = _get_signed_volumes_tetra(points, cells)

    assert len(volumes) == len(cells)
    assert np.all(np.sign(volumes) == 1)


if __name__ == "__main__":
    test_ball_tetra()
