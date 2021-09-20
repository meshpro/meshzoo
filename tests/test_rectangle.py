import numpy as np

import meshzoo

from .helpers import is_near_equal, signed_simplex_volumes


def test_up():
    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), 10, variant="up")
    assert len(points) == 121
    assert is_near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 200
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)

    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), (2, 1), variant="up")
    assert len(points) == 6
    assert is_near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert len(cells) == 4
    assert list(cells[0]) == [0, 1, 4]
    assert list(cells[2]) == [0, 4, 3]
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_zigzag():
    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), 10, variant="zigzag")
    assert len(points) == 121
    assert is_near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 200
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)

    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), 1, variant="zigzag")
    assert len(points) == 4
    assert is_near_equal(np.sum(points, axis=0), [2.0, 2.0])
    assert len(cells) == 2
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)

    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), (2, 1), variant="zigzag")
    assert len(points) == 6
    assert is_near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert len(cells) == 4
    assert list(cells[0]) == [0, 1, 4]
    assert list(cells[2]) == [1, 2, 4]
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_down():
    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), (4, 3), variant="down")
    assert len(points) == 20
    assert len(cells) == 24
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)
    # meshzoo.show2d(points, cells)


def test_center():
    points, cells = meshzoo.rectangle_tri((0, 0), (1, 1), (10, 8), variant="center")
    meshzoo.show2d(points, cells)
    assert len(points) == 99
    assert len(cells) == 160
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_quad():
    points, cells = meshzoo.rectangle_quad((0, 0), (1, 1), 10)
    assert len(points) == 121
    assert is_near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 100
    # meshzoo.save2d("rectangle-quad.svg", points, cells)
    points, cells = meshzoo.rectangle_quad((0, 0), (1, 1), (2, 1))
    assert len(points) == 6
    assert is_near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert len(cells) == 2
    assert list(cells[0]) == [0, 1, 4, 3]
    assert list(cells[1]) == [1, 2, 5, 4]

    points, cells = meshzoo.rectangle_quad((0, 0), (1, 1), (2, 2))
    assert len(points) == 9
    assert len(cells) == 4
    assert list(cells[0]) == [0, 1, 4, 3]
    assert list(cells[1]) == [3, 4, 7, 6]
    assert list(cells[2]) == [1, 2, 5, 4]
    assert list(cells[3]) == [4, 5, 8, 7]
