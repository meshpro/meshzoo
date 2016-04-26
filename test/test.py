# -*- coding: utf-8 -*-
#
import os
import sys

# add meshpy path, cf. <http://stackoverflow.com/a/9350788/353337>
sys.path.insert(
        0,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..',
            'meshpy'
            )
        )

import ball
import cube
import ellipse


def test_ball():
    points, cells = ball.create_ball_mesh(10)
    assert len(points) == 1360
    assert len(cells) == 5005
    return


def test_cube():
    points, cells = cube.create_cube_mesh(10)
    assert len(points) == 50
    assert len(cells) == 68
    return


def test_ellipse():
    points, cells = ellipse.create_ellipse_mesh([0.5, 1], 100)
    assert len(points) == 1444
    assert len(cells) == 2774
    return


if __name__ == '__main__':
    test_ball()
