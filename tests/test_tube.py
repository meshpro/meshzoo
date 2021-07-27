import numpy as np

import meshzoo

from .helpers import is_near_equal


def test_tube():
    points, cells = meshzoo.tube(n=10)
    assert len(points) == 20
    assert is_near_equal(np.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 20
