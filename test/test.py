# -*- coding: utf-8 -*-
#
import sys
sys.path.insert(0, '../meshpy/')

import ball
import cube

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

if __name__ == '__main__':
    test_gen()
