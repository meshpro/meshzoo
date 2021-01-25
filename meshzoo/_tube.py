import numpy as np


def tube(length=1.0, radius=1.0, n=30):
    # Number of nodes along the width of the strip (>= 2)
    # Choose it such that we have approximately square boxes.
    nw = int(round(length * n / (2 * np.pi * radius)))

    # Generate suitable ranges for parametrization
    u_range = np.linspace(0.0, 2 * np.pi, num=n, endpoint=False)
    v_range = np.linspace(-0.5 * length, 0.5 * length, num=nw)

    # Create the vertices.
    proto_nodes = np.dstack(np.meshgrid(u_range, v_range, indexing="ij")).reshape(-1, 2)
    nodes = np.column_stack(
        [
            radius * np.cos(proto_nodes[:, 0]),
            radius * np.sin(proto_nodes[:, 0]),
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

    return nodes, np.array(elems)
