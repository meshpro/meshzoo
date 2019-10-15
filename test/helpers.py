import numpy


def _near_equal(a, b, tol=1.0e-12):
    return numpy.allclose(a, b, rtol=0.0, atol=tol)
