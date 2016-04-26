# -*- coding: utf-8 -*-
#
import sys
sys.path.insert(0, '../meshpy/')

import ball


def test_gen():
    points, cells = ball.create_ball_mesh(10)
    assert len(points) == 1360
    assert len(cells) == 5005
    return

if __name__ == '__main__':
    test_gen()
