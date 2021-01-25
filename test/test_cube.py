import numpy as np

import meshzoo


def test_cube():
    points, cells = meshzoo.cube_tet((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 11)
    assert len(points) == 1331
    assert len(cells) == 5000

    points, cells = meshzoo.cube_tet((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 3)
    assert len(points) == 27
    assert all(np.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 40


def test_cube_hexa():
    points, cells = meshzoo.cube_hexa((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 11)
    assert len(points) == 1331
    assert len(cells) == 1000

    points, cells = meshzoo.cube_hexa((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 3)
    assert len(points) == 27
    assert all(np.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 8
