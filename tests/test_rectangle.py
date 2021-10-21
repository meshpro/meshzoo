import numpy as np

import meshzoo

from .helpers import is_near_equal, signed_simplex_volumes


def test_up():
    x_range = np.linspace(0.0, 1.0, 11)
    y_range = np.linspace(0.0, 1.0, 11)
    points, cells = meshzoo.rectangle_tri(x_range, y_range, variant="up")
    assert len(points) == 121
    assert is_near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 200
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_up2():
    x_range = np.linspace(0.0, 1.0, 3)
    y_range = np.linspace(0.0, 1.0, 2)
    points, cells = meshzoo.rectangle_tri(x_range, y_range, variant="up")
    assert len(points) == 6
    assert is_near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert len(cells) == 4
    assert list(cells[0]) == [0, 1, 4]
    assert list(cells[2]) == [0, 4, 3]
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_zigzag():
    x_range = np.linspace(0.0, 1.0, 11)
    y_range = np.linspace(0.0, 1.0, 11)
    points, cells = meshzoo.rectangle_tri(x_range, y_range, variant="zigzag")
    assert len(points) == 121
    assert is_near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 200
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_zigzag2():
    x_range = np.linspace(0.0, 1.0, 2)
    y_range = np.linspace(0.0, 1.0, 2)
    points, cells = meshzoo.rectangle_tri(x_range, y_range, variant="zigzag")
    assert len(points) == 4
    assert is_near_equal(np.sum(points, axis=0), [2.0, 2.0])
    assert len(cells) == 2
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_zigzag3():
    x_range = np.linspace(0.0, 1.0, 3)
    y_range = np.linspace(0.0, 1.0, 2)
    points, cells = meshzoo.rectangle_tri(x_range, y_range, variant="zigzag")
    assert len(points) == 6
    assert is_near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert len(cells) == 4
    assert list(cells[0]) == [0, 1, 4]
    assert list(cells[2]) == [1, 2, 4]
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_down():
    x_range = np.linspace(0.0, 1.0, 5)
    y_range = np.linspace(0.0, 1.0, 4)
    points, cells = meshzoo.rectangle_tri(x_range, y_range, variant="down")
    assert len(points) == 20
    assert len(cells) == 24
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)
    # meshzoo.show2d(points, cells)


def test_center():
    x_range = np.linspace(0.0, 1.0, 11)
    y_range = np.linspace(0.0, 1.0, 9)
    points, cells = meshzoo.rectangle_tri(x_range, y_range, variant="center")
    meshzoo.show2d(points, cells)
    assert len(points) == 99
    assert len(cells) == 160
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


def test_quad1():
    x_range = np.linspace(0.0, 1.0, 11)
    y_range = np.linspace(0.0, 1.0, 11)
    points, cells = meshzoo.rectangle_quad(x_range, y_range)
    assert len(points) == 121
    assert is_near_equal(np.sum(points, axis=0), [60.5, 60.5])
    assert len(cells) == 100
    # meshzoo.save2d("rectangle-quad.svg", points, cells)


def test_quad2():
    x_range = np.linspace(0.0, 1.0, 3)
    y_range = np.linspace(0.0, 1.0, 2)
    points, cells = meshzoo.rectangle_quad(x_range, y_range)
    assert len(points) == 6
    assert is_near_equal(np.sum(points, axis=0), [3.0, 3.0])
    assert np.all(cells == [[0, 1, 4, 3], [1, 2, 5, 4]])


def test_quad3():
    x_range = np.linspace(0.0, 1.0, 3)
    y_range = np.linspace(0.0, 1.0, 3)
    points, cells = meshzoo.rectangle_quad(x_range, y_range)
    assert len(points) == 9
    assert np.all(cells == [[0, 1, 4, 3], [3, 4, 7, 6], [1, 2, 5, 4], [4, 5, 8, 7]])


def test_quad8():
    x_range = np.linspace(0.0, 1.0, 3)
    y_range = np.linspace(0.0, 1.0, 2)
    points, cells = meshzoo.rectangle_quad(x_range, y_range, cell_type="quad8")
    assert len(points) == 13
    print(cells.tolist())
    assert np.all(cells == [[0, 1, 4, 3, 6, 11, 8, 10], [1, 2, 5, 4, 7, 12, 9, 11]])
