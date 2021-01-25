import numpy as np
from helpers import _get_signed_areas

import meshzoo


def test_ngon():
    points, cells = meshzoo.ngon(9, 8)
    assert len(points) == 325
    assert len(cells) == 576
    # meshzoo.save2d("9gon.svg", points, cells)
    assert np.all(_get_signed_areas(points.T, cells) > 0.0)


if __name__ == "__main__":
    test_ngon()
