import numpy


def uv_sphere(num_points_per_circle=20, num_circles=10, radius=1.0):
    # Mesh parameters
    n_phi = num_points_per_circle
    n_theta = num_circles

    # Generate suitable ranges for parametrization
    phi_range = numpy.linspace(0.0, 2 * numpy.pi, num=n_phi, endpoint=False)
    theta_range = numpy.linspace(
        -numpy.pi / 2 + numpy.pi / (n_theta - 1),
        numpy.pi / 2 - numpy.pi / (n_theta - 1),
        num=n_theta - 2,
    )

    num_nodes = len(theta_range) * len(phi_range) + 2
    nodes = numpy.empty(num_nodes, dtype=numpy.dtype((float, 3)))
    # south pole
    south_pole_index = 0
    k = 0
    nodes[k] = numpy.array([0.0, 0.0, -1.0])
    k += 1
    # nodes in the circles of latitude (except poles)
    for theta in theta_range:
        for phi in phi_range:
            nodes[k] = numpy.array(
                [
                    numpy.cos(theta) * numpy.sin(phi),
                    numpy.cos(theta) * numpy.cos(phi),
                    numpy.sin(theta),
                ]
            )
            k += 1
    # north pole
    north_pole_index = k
    nodes[k] = numpy.array([0.0, 0.0, 1.0])

    nodes *= radius

    # create the elements (cells)
    num_elems = 2 * (n_theta - 2) * n_phi
    elems = numpy.empty(num_elems, dtype=numpy.dtype((int, 3)))
    k = 0

    # connections to south pole
    for i in range(n_phi - 1):
        elems[k] = numpy.array([south_pole_index, i + 1, i + 2])
        k += 1
    # close geometry
    elems[k] = numpy.array([south_pole_index, n_phi, 1])
    k += 1

    # non-pole elements
    for i in range(n_theta - 3):
        for j in range(n_phi - 1):
            elems[k] = numpy.array(
                [i * n_phi + j + 1, i * n_phi + j + 2, (i + 1) * n_phi + j + 2]
            )
            k += 1
            elems[k] = numpy.array(
                [i * n_phi + j + 1, (i + 1) * n_phi + j + 2, (i + 1) * n_phi + j + 1]
            )
            k += 1

    # close the geometry
    for i in range(n_theta - 3):
        elems[k] = numpy.array([(i + 1) * n_phi, i * n_phi + 1, (i + 1) * n_phi + 1])
        k += 1
        elems[k] = numpy.array([(i + 1) * n_phi, (i + 1) * n_phi + 1, (i + 2) * n_phi])
        k += 1

    # connections to the north pole
    for i in range(n_phi - 1):
        elems[k] = numpy.array(
            [
                i + 1 + n_phi * (n_theta - 3) + 1,
                i + n_phi * (n_theta - 3) + 1,
                north_pole_index,
            ]
        )
        k += 1
    # close geometry
    elems[k] = numpy.array(
        [
            0 + n_phi * (n_theta - 3) + 1,
            n_phi - 1 + n_phi * (n_theta - 3) + 1,
            north_pole_index,
        ]
    )
    k += 1
    assert k == num_elems, "Wrong element count."

    return nodes, elems


def iso_sphere(n):
    assert n >= 1
    # Start off with an isosahedron and refine.

    # Construction from
    # <http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html>.
    # Create 12 vertices of a icosahedron.
    t = (1.0 + numpy.sqrt(5.0)) / 2.0
    vertices = []
    vertex_count = 0
    vertices += [
        numpy.array(
            [
                [-1, +t, +0],
                [+1, +t, +0],
                [-1, -t, +0],
                [+1, -t, +0],
                #
                [+0, -1, +t],
                [+0, +1, +t],
                [+0, -1, -t],
                [+0, +1, -t],
                #
                [+t, +0, -1],
                [+t, +0, +1],
                [-t, +0, -1],
                [-t, +0, +1],
            ]
        )
    ]
    vertex_count += len(vertices[-1])
    corner_nodes = numpy.arange(12)

    faces = [
        (0, 11, 5),
        (0, 5, 1),
        (0, 1, 7),
        (0, 7, 10),
        (0, 10, 11),
        (1, 5, 9),
        (5, 11, 4),
        (11, 10, 2),
        (10, 7, 6),
        (7, 1, 8),
        (3, 9, 4),
        (3, 4, 2),
        (3, 2, 6),
        (3, 6, 8),
        (3, 8, 9),
        (4, 9, 5),
        (2, 4, 11),
        (6, 2, 10),
        (8, 6, 7),
        (9, 8, 1),
    ]

    # create edges
    edges = set()
    for face in faces:
        edges.add(tuple(sorted([face[0], face[1]])))
        edges.add(tuple(sorted([face[1], face[2]])))
        edges.add(tuple(sorted([face[2], face[0]])))

    edges = list(edges)

    # create edge nodes:
    edge_nodes = {}
    t = numpy.linspace(1 / n, 1.0, n - 1, endpoint=False)
    corners = vertices[0]
    k = corners.shape[0]
    for edge in edges:
        i0, i1 = edge
        vertices += [numpy.outer(1 - t, corners[i0]) + numpy.outer(t, corners[i1])]
        vertex_count += len(vertices[-1])
        edge_nodes[edge] = numpy.arange(k, k + len(t))
        k += len(t)

    # This is the same code as appearing for cell in a single triangle. On each face,
    # those indices are translated into the actual indices.
    triangle_cells = []
    k = 0
    for i in range(n):
        for j in range(n - i):
            triangle_cells.append([k + j, k + j + 1, k + n - i + j + 1])
        for j in range(n - i - 1):
            triangle_cells.append([k + j + 1, k + n - i + j + 2, k + n - i + j + 1])
        k += n - i + 1
    triangle_cells = numpy.array(triangle_cells)

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
                numpy.hstack(
                    [
                        [numpy.full(n - i - 1, i), numpy.arange(1, n - i)]
                        for i in range(1, n)
                    ]
                )
                / n
            )
            bary = numpy.array([1.0 - bary[0] - bary[1], bary[1], bary[0]])
            corner_verts = numpy.array([vertices[0][i] for i in corners])
            vertices.append(numpy.dot(corner_verts.T, bary).T)
            num_new_vertices = len(vertices[-1])

        # translation table
        num_nodes_per_triangle = (n + 1) * (n + 2) // 2
        tt = numpy.empty(num_nodes_per_triangle, dtype=int)
        tt[:] = -1

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

        assert all(tt >= 0)  # TODO remove assertion

        cells += [tt[triangle_cells]]
        vertex_count += num_new_vertices

    vertices = numpy.concatenate(vertices)
    cells = numpy.concatenate(cells)

    # push all nodes to the sphere
    norms = numpy.sqrt(numpy.einsum("ij,ij->i", vertices, vertices))
    vertices = (vertices.T / norms.T).T

    return vertices, cells
