# -*- coding: utf-8 -*-
#
import os
import sys

import meshzoo


def test_cylinder():
    points, cells = \
        meshzoo.custom.cylinder_tri.create_cylinder_mesh()
    assert len(points) == 1000
    assert len(cells) == 1800
    return


def test_hexagon():
    points, cells = meshzoo.custom.hexagon.create_hexagon_mesh(2)
    assert len(points) == 61
    assert len(cells) == 96
    return


def test_moebius():
    points, cells = \
        meshzoo.custom.moebius_tri.create_moebius_mesh([100, 10], 1)
    assert len(points) == 1000
    assert len(cells) == 1800
    return


def test_moebius_alt():
    points, cells = \
        meshzoo.custom.moebius_tri_alt.create_mesh()
    assert len(points) == 5700
    assert len(cells) == 11020
    return


def test_moebius2():
    points, cells = \
        meshzoo.custom.moebius2_tri.create_mesh()
    assert len(points) == 5890
    assert len(cells) == 11400
    return


def test_pseudomoebius():
    points, cells = meshzoo.custom.pseudomoebius.create_mesh()
    assert len(points) == 5890
    assert len(cells) == 11400
    return


def test_simple_arrow():
    points, cells = meshzoo.custom.simple_arrow.create_mesh()
    assert len(points) == 5
    assert len(cells) == 4
    return


def test_simple_shell():
    points, cells = meshzoo.custom.simple_shell.create_mesh()
    assert len(points) == 5
    assert len(cells) == 4
    return


def test_sphere():
    points, cells = meshzoo.custom.sphere.create_mesh()
    assert len(points) == 162
    assert len(cells) == 320
    return


def test_triangle():
    points, cells = meshzoo.custom.triangle.create_mesh()
    assert len(points) == 15
    assert len(cells) == 16
    return


def test_tube():
    points, cells = meshzoo.custom.tube.create_mesh()
    assert len(points) == 150
    assert len(cells) == 240
    return


def test_ball():
    points, cells = meshzoo.meshpy.ball.create_ball_mesh(10)
    assert len(points) == 1360
    assert len(cells) == 5005
    return


def test_cube():
    points, cells = meshzoo.meshpy.cube.create_cube_mesh(10)
    assert len(points) == 50
    assert len(cells) == 68
    return


def test_ellipse():
    points, cells = meshzoo.meshpy.ellipse.create_mesh([0.5, 1], 100)
    assert len(points) == 1444
    assert len(cells) == 2774
    return


def test_lshape3d():
    points, cells = meshzoo.meshpy.lshape3d.create_mesh()
    assert len(points) == 943
    assert len(cells) == 3394
    return


def test_pacman():
    points, cells = meshzoo.meshpy.pacman.create_pacman_mesh()
    assert len(points) == 446
    assert len(cells) == 831
    return


def test_tetrahedron():
    points, cells = meshzoo.meshpy.tetrahedron.create_tetrahedron_mesh()
    assert len(points) == 604
    assert len(cells) == 1805
    return


def test_torus():
    points, cells = meshzoo.meshpy.torus.create_mesh()
    assert len(points) == 921
    assert len(cells) == 2681
    return


# Disable for now since Gmsh doesn't pass for the version installed on travis
# (trusty).
# def test_screw():
#     points, cells = meshzoo.pygmsh.screw.create_screw_mesh()
#     assert len(points) == 2412
#     assert len(cells) == 7934
#     return


# Disable for now since we need mshr in a dev version for mshr.Extrude2D
# def test_toy():
#     points, cells = meshzoo.mshr.toy.create_toy_mesh()
#     assert len(points) == 2760
#     assert len(cells) == 11779
#     return


if __name__ == '__main__':
    test_ball()
