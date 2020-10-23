import numpy


def rectangle(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, nx=11, ny=11, variant="zigzag"):
    # Create the vertices.
    x_range = numpy.linspace(xmin, xmax, nx)
    y_range = numpy.linspace(ymin, ymax, ny)
    nodes = numpy.array(numpy.meshgrid(x_range, y_range)).reshape(2, -1).T
    elem_fun = {"zigzag": _zigzag, "center": _center, "down": _down, "up": _up}
    return nodes, elem_fun[variant](nx, ny)


def _up(nx, ny):
    # a = [i + j*nx]
    a = numpy.add.outer(numpy.arange(nx - 1), nx * numpy.arange(ny - 1))
    elems0 = numpy.array([a, a + 1, a + nx + 1]).reshape(3, -1).T
    elems1 = numpy.array([a, a + 1 + nx, a + nx]).reshape(3, -1).T
    elems = numpy.concatenate([elems0, elems1])
    return elems


def _down(nx, ny):
    # a = [i + j*nx]
    a = numpy.add.outer(numpy.arange(nx - 1), nx * numpy.arange(ny - 1))
    elems0 = numpy.array([a, a + 1, a + nx]).reshape(3, -1).T
    elems1 = numpy.array([a + 1, a + 1 + nx, a + nx]).reshape(3, -1).T
    elems = numpy.concatenate([elems0, elems1])
    return elems


def _center(nx, ny):
    assert (
        nx % 2 == 1 and ny % 2 == 1
    ), "center mode only works with an odd number of cells"

    # Create the elements (cells).
    # a = [i + j*nx]
    a = numpy.add.outer(numpy.arange(nx - 1), nx * numpy.arange(ny - 1))

    elems = []
    nx2 = (nx - 1) // 2
    ny2 = (ny - 1) // 2

    # bottom left
    ax0 = a[:nx2, :ny2]
    elems.append(numpy.array([ax0, ax0 + 1, ax0 + nx + 1]).reshape(3, -1).T)
    elems.append(numpy.array([ax0, ax0 + 1 + nx, ax0 + nx]).reshape(3, -1).T)

    # bottom right
    ax0 = a[nx2:, :ny2]
    elems.append(numpy.array([ax0, ax0 + 1, ax0 + nx]).reshape(3, -1).T)
    elems.append(numpy.array([ax0 + 1, ax0 + 1 + nx, ax0 + nx]).reshape(3, -1).T)

    # top left
    ax0 = a[:nx2, ny2:]
    elems.append(numpy.array([ax0, ax0 + 1, ax0 + nx]).reshape(3, -1).T)
    elems.append(numpy.array([ax0 + 1, ax0 + 1 + nx, ax0 + nx]).reshape(3, -1).T)

    # top right
    ax0 = a[nx2:, ny2:]
    elems.append(numpy.array([ax0, ax0 + 1, ax0 + nx + 1]).reshape(3, -1).T)
    elems.append(numpy.array([ax0, ax0 + 1 + nx, ax0 + nx]).reshape(3, -1).T)

    elems = numpy.concatenate(elems)

    return elems


def _zigzag(nx, ny):
    # Create the elements (cells).
    # a = [i + j*nx]
    a = numpy.add.outer(numpy.arange(nx - 1), nx * numpy.arange(ny - 1))

    # [i + j*nx, i+1 + j*nx, i+1 + (j+1)*nx]
    elems0 = numpy.dstack([a, a + 1, a + nx + 1])
    # [i+1 + j*nx, i+1 + (j+1)*nx, i + (j+1)*nx] for "every other" element
    elems0[0::2, 1::2, 0] += 1
    elems0[1::2, 0::2, 0] += 1
    elems0[0::2, 1::2, 1] += nx
    elems0[1::2, 0::2, 1] += nx
    elems0[0::2, 1::2, 2] -= 1
    elems0[1::2, 0::2, 2] -= 1

    # [i + j*nx, i+1 + (j+1)*nx,  i + (j+1)*nx]
    elems1 = numpy.dstack([a, a + 1 + nx, a + nx])
    # [i + j*nx, i+1 + j*nx, i + (j+1)*nx] for "every other" element
    elems1[0::2, 1::2, 1] -= nx
    elems1[1::2, 0::2, 1] -= nx

    elems = numpy.concatenate([elems0.reshape(-1, 3), elems1.reshape(-1, 3)])
    return elems
