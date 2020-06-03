import meshzoo


def test_ngon():
    points, cells = meshzoo.ngon(9, 8)
    assert len(points) == 325
    assert len(cells) == 576
    meshzoo.show2d(points, cells)


if __name__ == "__main__":
    test_ngon()
