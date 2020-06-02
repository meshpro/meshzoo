import numpy

import meshzoo

from helpers import _near_equal


def test_rectangle():
    points, cells = meshzoo.rectangle(nx=11, ny=11, variant="up")
    assert len(points) == 121
    assert _near_equal(numpy.sum(points, axis=0), [60.5, 60.5, 0.0])
    assert len(cells) == 200

    points, cells = meshzoo.rectangle(nx=11, ny=11, variant="zigzag")
    assert len(points) == 121
    assert _near_equal(numpy.sum(points, axis=0), [60.5, 60.5, 0.0])
    assert len(cells) == 200

    points, cells = meshzoo.rectangle(nx=2, ny=2, variant="zigzag")
    assert len(points) == 4
    assert _near_equal(numpy.sum(points, axis=0), [2.0, 2.0, 0.0])
    assert len(cells) == 2

    points, cells = meshzoo.rectangle(nx=3, ny=2, variant="up")
    assert len(points) == 6
    assert _near_equal(numpy.sum(points, axis=0), [3.0, 3.0, 0.0])
    assert len(cells) == 4
    assert set(cells[0]) == {0, 1, 4}
    assert set(cells[2]) == {0, 3, 4}

    points, cells = meshzoo.rectangle(nx=3, ny=2, variant="zigzag")
    assert len(points) == 6
    assert _near_equal(numpy.sum(points, axis=0), [3.0, 3.0, 0.0])
    assert len(cells) == 4
    assert set(cells[0]) == {0, 1, 4}
    assert set(cells[2]) == {0, 3, 4}


def test_down():
    points, cells = meshzoo.rectangle(nx=5, ny=5, variant="down")
    meshzoo.show2d(points, cells)


if __name__ == "__main__":
    test_down()
