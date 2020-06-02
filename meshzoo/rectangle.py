import numpy


def rectangle(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, nx=11, ny=11, variant="zigzag"):
    if variant == "zigzag":
        return _zigzag(xmin, xmax, ymin, ymax, nx, ny)
    elif variant == "center":
        return _center(xmin, xmax, ymin, ymax, nx, ny)
    elif variant == "down":
        return _down(xmin, xmax, ymin, ymax, nx, ny)

    assert variant == "up"
    return _up(xmin, xmax, ymin, ymax, nx, ny)


def _up(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = numpy.linspace(xmin, xmax, nx)
    y_range = numpy.linspace(ymin, ymax, ny)
    nodes = numpy.array(numpy.meshgrid(x_range, y_range)).reshape(2, -1).T

    # Create the elements (cells).
    # a = [i + j*nx]
    a = numpy.add.outer(numpy.arange(nx - 1), nx * numpy.arange(ny - 1))
    elems0 = numpy.array([a, a + 1, a + nx + 1]).reshape(3, -1).T
    elems1 = numpy.array([a, a + 1 + nx, a + nx]).reshape(3, -1).T
    elems = numpy.concatenate([elems0, elems1])

    return nodes, elems


def _down(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = numpy.linspace(xmin, xmax, nx)
    y_range = numpy.linspace(ymin, ymax, ny)
    nodes = numpy.array(numpy.meshgrid(x_range, y_range)).reshape(2, -1).T

    # Create the elements (cells).
    # a = [i + j*nx]
    a = numpy.add.outer(numpy.arange(nx - 1), nx * numpy.arange(ny - 1))
    elems0 = numpy.array([a, a + 1, a + nx]).reshape(3, -1).T
    elems1 = numpy.array([a + 1, a + 1 + nx, a + nx]).reshape(3, -1).T
    elems = numpy.concatenate([elems0, elems1])

    return nodes, elems


def _center(xmin, xmax, ymin, ymax, nx, ny):
    assert (
        nx % 2 == 1 and ny % 2 == 1
    ), "center mode only works with an odd number of cells"
    # Create the vertices.
    x_range = numpy.linspace(xmin, xmax, nx)
    y_range = numpy.linspace(ymin, ymax, ny)
    nodes = numpy.array(numpy.meshgrid(x_range, y_range)).reshape(2, -1).T

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

    return nodes, elems


def _zigzag(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = numpy.linspace(xmin, xmax, nx)
    y_range = numpy.linspace(ymin, ymax, ny)
    nodes = numpy.array(numpy.meshgrid(x_range, y_range)).reshape(2, -1).T

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

    return nodes, elems
