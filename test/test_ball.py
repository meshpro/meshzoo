import meshzoo


def test_ball_hexa():
    points, cells = meshzoo.ball_hexa(11)
    assert len(points) == 1331
    assert len(cells) == 1000


def test_ball_tetra():
    points, cells = meshzoo.ball_tetra(11)
    # import meshio
    # meshio.Mesh(points, {"tetra": cells}).write("out.vtk")
    assert len(points) == 1331
    assert len(cells) == 5000
