import numpy as np
import pytest

import meshzoo

from .helpers import is_near_equal


@pytest.mark.parametrize(
    "num_twists, num_points, num_cells, ref1, ref2",
    [
        [1, 5890, 11400, [0, 0, 0], [2753575 / 9.0, 2724125 / 9.0, 58900 / 3.0]],
        [2, 5890, 11400, [0, 0, 0], [2797750 / 9.0, 2679950 / 9.0, 58900 / 3.0]],
    ],
)
def test_moebius(num_twists, num_points, num_cells, ref1, ref2):
    points, cells = meshzoo.moebius(num_twists, 190, 31, variant="smooth")
    assert len(points) == num_points
    assert len(cells) == num_cells
    assert is_near_equal(np.sum(points, axis=0), ref1, tol=1.0e-10)
    sum_points2 = np.sum(points**2, axis=0)
    assert np.allclose(sum_points2, ref2, rtol=1.0e-12, atol=0.0)


@pytest.mark.parametrize(
    "num_twists, num_points, num_cells, ref1, ref2",
    [
        [
            1,
            5700,
            11020,
            [0, 0, 0],
            [[296107.21982759, 292933.72844828, 19040.94827586]],
        ],
        [
            2,
            5700,
            11020,
            [0, 0, 0],
            [[300867.45689655, 288173.49137931, 19040.94827586]],
        ],
    ],
)
def test_moebius2(num_twists, num_points, num_cells, ref1, ref2):
    points, cells = meshzoo.moebius(
        nl=190, nw=30, num_twists=num_twists, variant="smooth"
    )
    assert len(points) == num_points
    assert len(cells) == num_cells
    assert is_near_equal(np.sum(points, axis=0), ref1, tol=1.0e-10)
    sum_points2 = np.sum(points**2, axis=0)
    assert np.allclose(sum_points2, ref2, rtol=1.0e-12, atol=0.0)


@pytest.mark.parametrize(
    "num_twists, num_points, num_cells, ref1, ref2",
    [
        [1, 1000, 1800, [0, 0, 0], [1418750 / 27.0, 1418750 / 27.0, 137500 / 27.0]],
        [2, 1000, 1800, [0, 0, 0], [484375 / 9.0, 1384375 / 27.0, 137500 / 27.0]],
    ],
)
def test_moebius3(num_twists, num_points, num_cells, ref1, ref2):
    points, cells = meshzoo.moebius(num_twists, 100, 10, variant="classical")
    assert len(points) == num_points
    assert len(cells) == num_cells
    assert is_near_equal(np.sum(points, axis=0), ref1, tol=1.0e-10)
    sum_points2 = np.sum(points**2, axis=0)
    assert np.allclose(sum_points2, ref2, rtol=1.0e-12, atol=0.0)


def test_pseudomoebius():
    points, cells = meshzoo.moebius(nl=190, nw=31, variant="pseudo")
    assert len(points) == 5890
    assert len(cells) == 11400
    assert is_near_equal(np.sum(points, axis=0), [0, 0, 0], tol=1.0e-10)
    sum_points2 = np.sum(points**2, axis=0)
    ref2 = [2753575 / 9.0, 2724125 / 9.0, 58900 / 3.0]
    assert np.allclose(sum_points2, ref2, rtol=1.0e-12, atol=0.0)
