import meshzoo

from .helpers import signed_simplex_volumes


def test_ball_hexa():
    points, cells = meshzoo.ball_hexa(10)
    # import meshio
    # meshio.Mesh(points, {"hexahedron": cells}).write("ball-hexa.vtk")
    assert len(points) == 1331
    assert len(cells) == 1000


def test_ball_tetra():
    points, cells = meshzoo.ball_tetra(10)
    # import meshio
    # meshio.Mesh(points, {"tetra": cells}).write("ball-tetra.vtk")
    assert len(points) == 1331
    assert len(cells) == 5000


def test_positive_volumes():
    points, cells = meshzoo.ball_tetra(2)
    assert (signed_simplex_volumes(points, cells) > 0.0).all()
