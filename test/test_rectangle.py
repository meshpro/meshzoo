import numpy as np
from helpers import _get_signed_areas, _near_equal

import meshzoo


def test_up():
    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), 11, variant="up")
    assert len(points) == 121
    assert _near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 200
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)

    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), (3, 2), variant="up")
    assert len(points) == 6
    assert _near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert len(cells) == 4
    assert set(cells[0]) == {0, 1, 4}
    assert set(cells[2]) == {0, 3, 4}
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)


def test_zigzag():
    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), 11, variant="zigzag")
    assert len(points) == 121
    assert _near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 200
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)

    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), 2, variant="zigzag")
    assert len(points) == 4
    assert _near_equal(np.sum(points, axis=0), [2.0, 2.0])
    assert len(cells) == 2
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)

    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), (3, 2), variant="zigzag")
    assert len(points) == 6
    assert _near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert len(cells) == 4
    assert set(cells[0]) == {0, 1, 4}
    assert set(cells[2]) == {0, 3, 4}
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)


def test_down():
    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), (5, 4), variant="down")
    assert len(points) == 20
    assert len(cells) == 24
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)
    # meshzoo.show2d(points, cells)


def test_center():
    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), (11, 9), variant="center")
    meshzoo.show2d(points, cells)
    assert len(points) == 99
    assert len(cells) == 160
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)


def test_quad():
    points, cells = meshzoo.rectangle_quad((0, 0), (1, 1), 11)
    assert len(points) == 121
    assert _near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 100
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)

    points, cells = meshzoo.rectangle_quad((0, 0), (1, 1), (3, 2))
    assert len(points) == 6
    assert _near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert len(cells) == 2
    assert set(cells[0]) == {0, 1, 3, 4}
    assert set(cells[1]) == {1, 2, 4, 5}
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)


if __name__ == "__main__":
    test_center()
