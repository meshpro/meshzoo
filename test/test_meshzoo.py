import numpy as np
from helpers import _near_equal

import meshzoo


def test_simple_arrow():
    points, cells = meshzoo.simple_arrow()
    assert len(points) == 5
    assert _near_equal(np.sum(points, axis=0), [7.0, 0.0, 0.0])
    assert len(cells) == 4


def test_simple_shell():
    points, cells = meshzoo.simple_shell()
    assert len(points) == 5
    assert _near_equal(np.sum(points, axis=0), [0.0, 0.0, 1.0])
    assert len(cells) == 4


def test_tube():
    points, cells = meshzoo.tube(n=10)
    assert len(points) == 20
    assert _near_equal(np.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 20


# def test_ball():
#     points, cells = meshzoo.meshpy.ball.create_ball_mesh(10)
#     assert len(points) == 1360
#     assert len(cells) == 5005
#
#
# def test_cube():
#     points, cells = meshzoo.meshpy.cube.create_mesh(10)
#     assert len(points) == 50
#     assert len(cells) == 68
#
#
# def test_ellipse():
#     points, cells = meshzoo.meshpy.ellipse.create_mesh(0.5, 1, 100)
#     assert len(points) == 1444
#     assert len(cells) == 2774
#
#
# def test_lshape():
#     points, cells = meshzoo.meshpy.lshape.create_mesh()
#     assert len(points) == 38
#     assert len(cells) == 58
#
#
# def test_lshape3d():
#     points, cells = meshzoo.meshpy.lshape3d.create_mesh()
#     assert len(points) == 943
#     assert len(cells) == 3394
#
#
# def test_pacman():
#     points, cells = meshzoo.meshpy.pacman.create_pacman_mesh()
#     assert len(points) == 446
#     assert len(cells) == 831
#
#
# def test_rectangle():
#     points, cells = meshzoo.meshpy.rectangle.create_mesh()
#     assert len(points) == 88
#     assert len(cells) == 150
#
#
# def test_rectangle_with_hole():
#     points, cells = meshzoo.meshpy.rectangle_with_hole.create_mesh()
#     assert len(points) == 570
#     assert len(cells) == 964
#
#
# def test_tetrahedron():
#     points, cells = meshzoo.meshpy.tetrahedron.create_tetrahedron_mesh()
#     assert len(points) == 604
#     assert len(cells) == 1805
#
#
# def test_torus():
#     points, cells = meshzoo.meshpy.torus.create_mesh()
#     assert len(points) == 921
#     assert len(cells) == 2681


# Disable for now since Gmsh doesn't pass for the version installed on travis
# (trusty).
# def test_screw():
#     points, cells = meshzoo.pygmsh.screw.create_screw_mesh()
#     assert len(points) == 2412
#     assert len(cells) == 7934


# Disable for now since we need mshr in a dev version for mshr.Extrude2D
# def test_toy():
#     points, cells = meshzoo.mshr.toy.create_toy_mesh()
#     assert len(points) == 2760
#     assert len(cells) == 11779


# if __name__ == '__main__':
#     test_plot2d()
#     # import meshio
#     # points_, cells_ = meshzoo.triangle(7)
#     # meshio.write('triangle.vtu', points_, {'triangle': cells_})
#     # points_, cells_ = meshzoo.cube()
#     # meshio.write('cube.vtu', points_, {'tetra': cells_})
