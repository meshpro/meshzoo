import meshzoo


def test_ngon():
    points, cells = meshzoo.ngon(8, 10)
    assert len(points) == 441
    assert len(cells) == 800
    meshzoo.show2d(points, cells)


if __name__ == "__main__":
    test_ngon()
