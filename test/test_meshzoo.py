# -*- coding: utf-8 -*-
#
import numpy
import meshzoo


def _near_equal(a, b, tol=1.0e-12):
    return numpy.allclose(a, b, rtol=0.0, atol=tol)


def test_cube():
    points, cells = meshzoo.cube()
    assert len(points) == 1331
    assert len(cells) == 5000

    points, cells = meshzoo.cube(nx=3, ny=3, nz=3)
    assert len(points) == 27
    assert all(numpy.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 40
    return


def test_cylinder():
    points, cells = meshzoo.cylinder()
    assert len(points) == 1000
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 1800
    return


def test_hexagon():
    points, cells = meshzoo.hexagon(2)
    assert len(points) == 61
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 96
    return


def test_moebius():
    points, cells = meshzoo.moebius()
    assert len(points) == 5890
    assert _near_equal(
            numpy.sum(points, axis=0),
            [-4.10009804e-11, -8.85214124e-12, -1.43687579e-13]
            )
    assert len(cells) == 11400

    points, cells = meshzoo.moebius(moebius_index=2)
    assert len(points) == 5890
    assert _near_equal(
            numpy.sum(points, axis=0),
            [4.72333284e-12, 4.80460116e-12, 1.88295560e-14]
            )
    assert len(cells) == 11400
    return


def test_moebius2():
    points, cells = meshzoo.moebius2()
    assert len(points) == 5700
    assert _near_equal(
            numpy.sum(points, axis=0),
            [-6.55155930e-11, 8.95811203e-13, -1.15784118e-13]
            )
    assert len(cells) == 11020

    points, cells = meshzoo.moebius2(moebius_index=2)
    assert len(points) == 5700
    assert _near_equal(
        numpy.sum(points, axis=0),
        [1.83320026e-12, 2.43982612e-12, -1.11195775e-14]
        )
    assert len(cells) == 11020
    return


def test_moebius3():
    points, cells = meshzoo.moebius3(100, 10, 1)
    assert len(points) == 1000
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 1800

    points, cells = meshzoo.moebius3(100, 10, 2)
    assert len(points) == 1000
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 1800
    return


def test_pseudomoebius():
    points, cells = meshzoo.pseudomoebius()
    assert len(points) == 5890
    assert _near_equal(
        numpy.sum(points, axis=0),
        [-4.10009804e-11, -8.85214124e-12, 1.43687579e-13]
        )
    assert len(cells) == 11400
    return


def test_rectangle():
    points, cells = meshzoo.rectangle(nx=11, ny=11, zigzag=False)
    assert len(points) == 121
    assert _near_equal(numpy.sum(points, axis=0), [60.5, 60.5, 0.0])
    assert len(cells) == 200

    points, cells = meshzoo.rectangle(nx=11, ny=11, zigzag=True)
    assert len(points) == 121
    assert _near_equal(numpy.sum(points, axis=0), [60.5, 60.5, 0.0])
    assert len(cells) == 200

    points, cells = meshzoo.rectangle(nx=2, ny=2, zigzag=True)
    assert len(points) == 4
    assert _near_equal(numpy.sum(points, axis=0), [2.0, 2.0, 0.0])
    assert len(cells) == 2

    points, cells = meshzoo.rectangle(nx=3, ny=2, zigzag=False)
    assert len(points) == 6
    assert _near_equal(numpy.sum(points, axis=0), [3.0, 3.0, 0.0])
    assert len(cells) == 4
    assert set(cells[0]) == set([0, 1, 4])
    assert set(cells[2]) == set([0, 3, 4])

    points, cells = meshzoo.rectangle(nx=3, ny=2, zigzag=True)
    assert len(points) == 6
    assert _near_equal(numpy.sum(points, axis=0), [3.0, 3.0, 0.0])
    assert len(cells) == 4
    assert set(cells[0]) == set([0, 1, 4])
    assert set(cells[2]) == set([0, 3, 4])

    return


def test_simple_arrow():
    points, cells = meshzoo.simple_arrow()
    assert len(points) == 5
    assert _near_equal(numpy.sum(points, axis=0), [7.0, 0.0, 0.0])
    assert len(cells) == 4
    return


def test_simple_shell():
    points, cells = meshzoo.simple_shell()
    assert len(points) == 5
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 1.0])
    assert len(cells) == 4
    return


def test_uv_sphere():
    points, cells = meshzoo.uv_sphere()
    assert len(points) == 162
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 320
    return


def test_iso_sphere():
    points, cells = meshzoo.iso_sphere()
    assert len(points) == 2562
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 5120
    return


def test_triangle():
    points, cells = meshzoo.triangle()
    assert len(points) == 15
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 16
    return


def test_tube():
    points, cells = meshzoo.tube(n=10)
    assert len(points) == 80
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 140
    return


# def test_ball():
#     points, cells = meshzoo.meshpy.ball.create_ball_mesh(10)
#     assert len(points) == 1360
#     assert len(cells) == 5005
#     return
#
#
# def test_cube():
#     points, cells = meshzoo.meshpy.cube.create_mesh(10)
#     assert len(points) == 50
#     assert len(cells) == 68
#     return
#
#
# def test_ellipse():
#     points, cells = meshzoo.meshpy.ellipse.create_mesh(0.5, 1, 100)
#     assert len(points) == 1444
#     assert len(cells) == 2774
#     return
#
#
# def test_lshape():
#     points, cells = meshzoo.meshpy.lshape.create_mesh()
#     assert len(points) == 38
#     assert len(cells) == 58
#     return
#
#
# def test_lshape3d():
#     points, cells = meshzoo.meshpy.lshape3d.create_mesh()
#     assert len(points) == 943
#     assert len(cells) == 3394
#     return
#
#
# def test_pacman():
#     points, cells = meshzoo.meshpy.pacman.create_pacman_mesh()
#     assert len(points) == 446
#     assert len(cells) == 831
#     return
#
#
# def test_rectangle():
#     points, cells = meshzoo.meshpy.rectangle.create_mesh()
#     assert len(points) == 88
#     assert len(cells) == 150
#     return
#
#
# def test_rectangle_with_hole():
#     points, cells = meshzoo.meshpy.rectangle_with_hole.create_mesh()
#     assert len(points) == 570
#     assert len(cells) == 964
#     return
#
#
# def test_tetrahedron():
#     points, cells = meshzoo.meshpy.tetrahedron.create_tetrahedron_mesh()
#     assert len(points) == 604
#     assert len(cells) == 1805
#     return
#
#
# def test_torus():
#     points, cells = meshzoo.meshpy.torus.create_mesh()
#     assert len(points) == 921
#     assert len(cells) == 2681
#     return


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
    import meshio
    points, cells = meshzoo.tube()
    meshio.write('tube.vtu', points, {'triangle': cells})
    # points, cells = meshzoo.cube()
    # meshio.write('cube.vtu', points, {'tetra': cells})
