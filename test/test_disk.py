import meshzoo


def test_disk():
    points, cells = meshzoo.disk(9, 8)
    assert len(points) == 325
    assert len(cells) == 576
    # meshzoo.save2d("4gon_disk.svg", points, cells)


if __name__ == "__main__":
    test_disk()
