# -*- coding: utf-8 -*-
#
from __future__ import division

import numpy


def triangle(n, corners=None):
    if corners is None:
        corners = [
            [0.0, 1.0, 0.0],
            [-0.5*numpy.sqrt(3.0), -0.5, 0.0],
            [+0.5*numpy.sqrt(3.0), -0.5, 0.0],
            ]
    corners = numpy.array(corners)

    h = 1/n
    bary = numpy.hstack([[
        numpy.full(n-i+1, i*h),
        numpy.arange(0, n-i+1) * h,
        ] for i in range(n+1)
        ])
    bary = numpy.array([bary[0], bary[1], 1.0 - bary[0] - bary[1]])
    points = numpy.dot(corners.T, bary).T

    # First create the mesh in barycentric coordinates
    cells = []
    k = 0
    for i in range(n):
        for j in range(n-i):
            cells.append([k+j, k+j+1, k+n-i+j+1])
        for j in range(n-i-1):
            cells.append([k+j+1, k+n-i+j+2, k+n-i+j+1])
        k += n-i+1
    cells = numpy.array(cells)

    return points, cells
