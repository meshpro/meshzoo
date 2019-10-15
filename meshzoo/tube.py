import numpy


def tube(length=1.0, radius=1.0, n=30):
    # Number of nodes along the width of the strip (>= 2)
    # Choose it such that we have approximately square boxes.
    nw = int(round(length * n / (2 * numpy.pi * radius)))

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2 * numpy.pi, num=n, endpoint=False)
    v_range = numpy.linspace(-0.5 * length, 0.5 * length, num=nw)

    # Create the vertices.
    proto_nodes = numpy.dstack(numpy.meshgrid(u_range, v_range, indexing="ij")).reshape(
        -1, 2
    )
    nodes = numpy.column_stack(
        [
            radius * numpy.cos(proto_nodes[:, 0]),
            radius * numpy.sin(proto_nodes[:, 0]),
            proto_nodes[:, 1],
        ]
    )

    # create the elements (cells)
    elems = []
    for i in range(n - 1):
        for j in range(nw - 1):
            elems.append([i * nw + j, (i + 1) * nw + j + 1, i * nw + j + 1])
            elems.append([i * nw + j, (i + 1) * nw + j, (i + 1) * nw + j + 1])

    # close the geometry
    for j in range(nw - 1):
        elems.append([(n - 1) * nw + j, j + 1, (n - 1) * nw + j + 1])
        elems.append([(n - 1) * nw + j, j, j + 1])

    return nodes, numpy.array(elems)
