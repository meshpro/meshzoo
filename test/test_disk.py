import meshzoo


def test_tri_disk():
    points, cells = meshzoo.tri_disk(15)
    assert len(points) == 136
    assert len(cells) == 225
    # meshzoo.save2d("tri_disk.svg", points, cells)


def test_quad_disk():
    points, cells = meshzoo.quad_disk(21)
    assert len(points) == 441
    assert len(cells) == 800
    # meshzoo.save2d("quad_disk.svg", points, cells)


def test_ngon_disk():
    points, cells = meshzoo.ngon_disk(6, 8)
    assert len(points) == 325
    assert len(cells) == 576
    # meshzoo.save2d("ngon_disk.svg", points, cells)


if __name__ == "__main__":
    test_ngon_disk()
