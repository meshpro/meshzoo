import numpy as np


def create_edges(cells_nodes):
    """Setup edge-node and edge-cell relations. Adapted from voropy."""
    # Create the idx_hierarchy (nodes->edges->cells), i.e., the value of
    # `self.idx_hierarchy[0, 2, 27]` is the index of the node of cell 27, edge
    # 2, node 0. The shape of `self.idx_hierarchy` is `(2, 3, n)`, where `n` is
    # the number of cells. Make sure that the k-th edge is opposite of the k-th
    # point in the triangle.
    local_idx = np.array([[1, 2], [2, 0], [0, 1]]).T
    # Map idx back to the nodes. This is useful if quantities which are in
    # idx shape need to be added up into nodes (e.g., equation system rhs).
    nds = cells_nodes.T
    idx_hierarchy = nds[local_idx]

    s = idx_hierarchy.shape
    a = np.sort(idx_hierarchy.reshape(s[0], s[1] * s[2]).T)

    b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx, inv, cts = np.unique(
        b, return_index=True, return_inverse=True, return_counts=True
    )

    # No edge has more than 2 cells. This assertion fails, for example, if
    # cells are listed twice.
    assert all(cts < 3)

    edge_nodes = a[idx]
    cells_edges = inv.reshape(3, -1).T

    return edge_nodes, cells_edges


def show2d(*args, **kwargs):
    import matplotlib.pyplot as plt

    plot2d(*args, **kwargs)
    plt.show()


def save2d(filename, *args, **kwargs):
    import matplotlib.pyplot as plt

    plot2d(*args, **kwargs)
    plt.savefig(filename, transparent=True, bbox_inches="tight")


def plot2d(
    points,
    cells,
    show_axes=False,
    # ParaView's default colors
    fill: str = "#c8c5bd",
    stroke: str = "#000080",
):
    """Plot a 2D mesh using matplotlib."""
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.gca()
    plt.axis("equal")
    if not show_axes:
        ax.set_axis_off()

    assert points.shape[1] == 2

    xmin = np.amin(points[:, 0])
    xmax = np.amax(points[:, 0])
    ymin = np.amin(points[:, 1])
    ymax = np.amax(points[:, 1])

    width = xmax - xmin
    xmin -= 0.1 * width
    xmax += 0.1 * width

    height = ymax - ymin
    ymin -= 0.1 * height
    ymax += 0.1 * height

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    for cell in cells:
        import matplotlib.patches

        poly = matplotlib.patches.Polygon(points[cell], ec=stroke, fc=fill)
        ax.add_patch(poly)

    # import matplotlib.tri
    # tri = matplotlib.tri.Triangulation(points[:,0], points[:,1], triangles=cells)
    # ax.triplot(tri, '-', lw=1, color="k")
    return fig


def _compose_from_faces(corners, faces, n, edge_adjust=None, face_adjust=None):
    # create corner nodes
    vertices = [corners]
    vertex_count = len(corners)
    corner_nodes = np.arange(len(corners))

    # create edges
    edges = set()
    for face in faces:
        edges.add(tuple(sorted([face[0], face[1]])))
        edges.add(tuple(sorted([face[1], face[2]])))
        edges.add(tuple(sorted([face[2], face[0]])))

    edges = list(edges)

    # create edge nodes:
    edge_nodes = {}
    t = np.linspace(1 / n, 1.0, n - 1, endpoint=False)
    corners = vertices[0]
    k = corners.shape[0]
    for edge in edges:
        i0, i1 = edge
        new_vertices = np.outer(1 - t, corners[i0]) + np.outer(t, corners[i1])
        if edge_adjust:
            new_vertices = edge_adjust(edge, new_vertices)
        vertices.append(new_vertices)
        vertex_count += len(vertices[-1])
        edge_nodes[edge] = np.arange(k, k + len(t))
        k += len(t)

    # This is the same code as appearing for cell in a single triangle. On each face,
    # those indices are translated into the actual indices.
    triangle_cells = []
    k = 0
    for i in range(n):
        j = np.arange(n - i)
        triangle_cells.append(np.column_stack([k + j, k + j + 1, k + n - i + j + 1]))
        j = j[:-1]
        triangle_cells.append(
            np.column_stack([k + j + 1, k + n - i + j + 2, k + n - i + j + 1])
        )
        k += n - i + 1
    triangle_cells = np.vstack(triangle_cells)

    cells = []
    for face in faces:
        corners = face
        edges = [(face[0], face[1]), (face[1], face[2]), (face[2], face[0])]
        is_edge_reverted = [False, False, False]
        for k, edge in enumerate(edges):
            if edge[0] > edge[1]:
                edges[k] = (edge[1], edge[0])
                is_edge_reverted[k] = True

        # First create the interior points in barycentric coordinates
        if n == 1:
            num_new_vertices = 0
        else:
            bary = (
                np.hstack(
                    [[np.full(n - i - 1, i), np.arange(1, n - i)] for i in range(1, n)]
                )
                / n
            )
            bary = np.array([1.0 - bary[0] - bary[1], bary[1], bary[0]])
            corner_verts = np.array([vertices[0][i] for i in corners])
            vertices_cart = np.dot(corner_verts.T, bary).T

            if face_adjust:
                vertices_cart = face_adjust(face, bary, vertices_cart, corner_verts)

            vertices.append(vertices_cart)
            num_new_vertices = len(vertices[-1])

        # translation table
        num_nodes_per_triangle = (n + 1) * (n + 2) // 2
        tt = np.empty(num_nodes_per_triangle, dtype=int)

        # first the corners
        tt[0] = corner_nodes[corners[0]]
        tt[n] = corner_nodes[corners[1]]
        tt[num_nodes_per_triangle - 1] = corner_nodes[corners[2]]
        # then the edges.
        # edge 0
        tt[1:n] = edge_nodes[edges[0]]
        if is_edge_reverted[0]:
            tt[1:n] = tt[1:n][::-1]
        #
        # edge 1
        idx = 2 * n
        for k in range(n - 1):
            if is_edge_reverted[1]:
                tt[idx] = edge_nodes[edges[1]][n - 2 - k]
            else:
                tt[idx] = edge_nodes[edges[1]][k]
            idx += n - k - 1
        #
        # edge 2
        idx = n + 1
        for k in range(n - 1):
            if is_edge_reverted[2]:
                tt[idx] = edge_nodes[edges[2]][k]
            else:
                tt[idx] = edge_nodes[edges[2]][n - 2 - k]
            idx += n - k

        # now the remaining interior nodes
        idx = n + 2
        j = vertex_count
        for k in range(n - 2):
            for _ in range(n - k - 2):
                tt[idx] = j
                j += 1
                idx += 1
            idx += 2

        cells += [tt[triangle_cells]]
        vertex_count += num_new_vertices

    vertices = np.concatenate(vertices)
    cells = np.concatenate(cells)

    return vertices, cells


def insert_midpoints_edges(points, cells, cell_type):
    """Collect all unique edges, calculate and return points including
    midpoints on edges as well as the extended cells array."""

    number_of_points = {"triangle": 3, "tetra": 4, "quad": 4, "hexahedron": 8}

    if cells.shape[1] != number_of_points[cell_type]:
        raise ValueError("Mismatch of cell type and shape of cells array.")

    if cell_type == "triangle":
        # k-th edge between cell points no. (ij[k])
        ij = [[0, 1], [1, 2], [2, 0]]

    elif cell_type == "tetra":
        # k-th edge between cell points no. (ij[k])
        ij = [[0, 1], [1, 2], [2, 0], [3, 0], [3, 1], [3, 2]]

    elif cell_type == "quad":
        # k-th edge between cell points no. (ij[k])
        ij = [[0, 1], [1, 2], [2, 3], [3, 0]]

    elif cell_type == "hexahedron":
        # k-th edge between cell points no. (ij[k])
        ij = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
        ]

    else:
        raise TypeError("Cell type not implemented.")

    # obtain edges from cells (contains duplicates)
    edges = cells[:, ij]

    # sort points of edges
    edges_sorted = np.sort(edges.reshape(-1, 2), axis=1)

    # obtain unique edges and inverse mapping
    edges_unique, inverse = np.unique(
        edges_sorted,
        return_index=False,
        return_inverse=True,
        return_counts=False,
        axis=0,
    )

    # calculate midpoints on edges as mean of edge-based pairs of points
    midpoints_on_edges = np.mean(points[edges_unique.T], axis=0)

    # create the additional cells array
    # add offset to point index for midpoints on edges
    cells_edges = inverse.reshape(len(cells), -1) + len(points)

    # vertical stack of points and horizontal stack of edges
    points_new = np.vstack((points, midpoints_on_edges))
    cells_new = np.hstack((cells, cells_edges))

    return points_new, cells_new
