import numpy
import meshzoo
from helpers import _near_equal


def test_triangle():
    points, cells = meshzoo.triangle(4)
    assert len(points) == 15
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0])
    assert len(cells) == 16
