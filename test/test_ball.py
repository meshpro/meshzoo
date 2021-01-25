import meshzoo


def test_ball_hexa():
    points, cells = meshzoo.ball_hexa(11)
    assert len(points) == 1331
    assert len(cells) == 1000
