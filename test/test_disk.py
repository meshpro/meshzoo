import meshzoo


def test_tri_disk():
    points, cells = meshzoo.tri_disk(15)
    assert len(points) == 136
    assert len(cells) == 225
    # meshzoo.show2d(points, cells)


def test_quad_disk():
    points, cells = meshzoo.quad_disk(15)
    assert len(points) == 225
    assert len(cells) == 392
    meshzoo.show2d(points, cells)


if __name__ == "__main__":
    test_quad_disk()
