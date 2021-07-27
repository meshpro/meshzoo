import meshzoo

from .helpers import signed_simplex_volumes


def test_disk():
    points, cells = meshzoo.disk(9, 8)
    meshzoo.save2d("4gon_disk.svg", points, cells)
    assert len(points) == 325
    assert len(cells) == 576
    assert (signed_simplex_volumes(points, cells) > 0.0).all()


def test_disk_quad():
    points, cells = meshzoo.disk_quad(10)
    # meshzoo.save2d("disk-quad.svg", points, cells)
    assert len(points) == 121
    assert len(cells) == 100
