import meshzoo


def test_tri_disk():
    points, cells = meshzoo.tri_disk(15)
    assert len(points) == 136
    assert len(cells) == 225
    # meshzoo.show2d(points, cells)
