import numpy as np

import meshzoo

from .helpers import signed_simplex_volumes


def test_ngon():
    points, cells = meshzoo.ngon(9, 8)
    # meshzoo.save2d("9gon.svg", points, cells)
    assert len(points) == 325
    assert len(cells) == 576
    assert np.all(signed_simplex_volumes(points, cells) > 0.0)


if __name__ == "__main__":
    test_ngon()
