import numpy
import meshzoo
from helpers import _get_signed_areas


def test_ngon():
    points, cells = meshzoo.ngon(9, 8)
    assert points.shape[1] == 325
    assert len(cells) == 576
    # meshzoo.save2d("9gon.svg", points, cells)
    assert numpy.all(_get_signed_areas(points, cells) > 0.0)


if __name__ == "__main__":
    test_ngon()
