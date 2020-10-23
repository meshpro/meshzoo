from helpers import _get_signed_areas

import meshzoo


def test_disk():
    points, cells = meshzoo.disk(9, 8)
    assert points.shape[1] == 325
    assert len(cells) == 576
    # meshzoo.save2d("4gon_disk.svg", points, cells)
    assert (_get_signed_areas(points, cells) > 0.0).all()


if __name__ == "__main__":
    test_disk()
