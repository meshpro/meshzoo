import numpy as np

from ._helpers import _compose_from_faces


def uv_sphere(num_points_per_circle: int, num_circles: int, radius: float = 1.0):
    # Mesh parameters
    n_phi = num_points_per_circle
    n_theta = num_circles

    # Generate suitable ranges for parametrization
    phi_range = np.linspace(0.0, 2 * np.pi, num=n_phi, endpoint=False)
    theta_range = np.linspace(
        -np.pi / 2 + np.pi / (n_theta - 1),
        np.pi / 2 - np.pi / (n_theta - 1),
        num=n_theta - 2,
    )

    # nodes in the circles of latitude (except poles)
    nodes = radius * np.array(
        [[0.0, 0.0, -1.0]]  # south pole
        + [
            [
                np.cos(theta) * np.sin(phi),
                np.cos(theta) * np.cos(phi),
                np.sin(theta),
            ]
            for theta in theta_range
            for phi in phi_range
        ]
        + [[0.0, 0.0, 1.0]]  # north pole
    )

    south_pole_index = 0
    north_pole_index = len(nodes) - 1

    # create the elements (cells)
    num_cells = 2 * (n_theta - 2) * n_phi
    cells = []

    # connections to south pole
    for i in range(n_phi - 1):
        cells.append([south_pole_index, i + 1, i + 2])
    # close geometry
    cells.append([south_pole_index, n_phi, 1])

    # non-pole elements
    for i in range(n_theta - 3):
        for j in range(n_phi - 1):
            cells += [
                [i * n_phi + j + 2, i * n_phi + j + 1, (i + 1) * n_phi + j + 2],
                [i * n_phi + j + 1, (i + 1) * n_phi + j + 1, (i + 1) * n_phi + j + 2],
            ]

    # close the geometry
    for i in range(n_theta - 3):
        cells += [
            [i * n_phi + 1, (i + 1) * n_phi, (i + 1) * n_phi + 1],
            [(i + 1) * n_phi + 1, (i + 1) * n_phi, (i + 2) * n_phi],
        ]

    # connections to the north pole
    for i in range(n_phi - 1):
        cells.append(
            [
                i + 1 + n_phi * (n_theta - 3) + 1,
                i + n_phi * (n_theta - 3) + 1,
                north_pole_index,
            ]
        )
    # close geometry
    cells.append(
        [
            0 + n_phi * (n_theta - 3) + 1,
            n_phi - 1 + n_phi * (n_theta - 3) + 1,
            north_pole_index,
        ]
    )
    cells = np.array(cells)
    assert len(cells) == num_cells, "Wrong element count."

    return nodes, cells


def geo_sphere(num_points_per_circle: int, num_circles: int, radius=1.0):
    # Mesh parameters
    n_phi = num_points_per_circle
    n_theta = num_circles

    # Generate suitable ranges for parametrization
    phi_range = np.linspace(0.0, 2 * np.pi, num=n_phi, endpoint=False)
    theta_range = np.linspace(
        -np.pi / 2 + np.pi / (n_theta - 1),
        np.pi / 2 - np.pi / (n_theta - 1),
        num=n_theta - 2,
    )

    # nodes in the circles of latitude (except poles)
    nodes = radius * np.array(
        [[0.0, 0.0, -1.0]]  # south pole
        + [
            [
                np.cos(theta) * np.sin(phi),
                np.cos(theta) * np.cos(phi),
                np.sin(theta),
            ]
            for theta in theta_range
            for phi in phi_range
        ]
        + [[0.0, 0.0, 1.0]]  # north pole
    )

    south_pole_index = 0
    north_pole_index = len(nodes) - 1

    # create the elements (cells)
    tri = []
    quad = []

    # connections to south pole
    for i in range(n_phi - 1):
        tri.append([south_pole_index, i + 1, i + 2])
    # close geometry
    tri.append([south_pole_index, n_phi, 1])

    # non-pole elements
    for i in range(n_theta - 3):
        for j in range(n_phi - 1):
            quad += [
                [
                    i * n_phi + j + 1,
                    i * n_phi + j + 2,
                    (i + 1) * n_phi + j + 2,
                    (i + 1) * n_phi + j + 1,
                ],
            ]

    # close the geometry
    for i in range(n_theta - 3):
        quad += [
            [i * n_phi + 1, (i + 1) * n_phi + 1, (i + 2) * n_phi, (i + 1) * n_phi],
        ]

    # connections to the north pole
    for i in range(n_phi - 1):
        tri.append(
            [
                i + 1 + n_phi * (n_theta - 3) + 1,
                i + n_phi * (n_theta - 3) + 1,
                north_pole_index,
            ]
        )
    # close geometry
    tri.append(
        [
            0 + n_phi * (n_theta - 3) + 1,
            n_phi - 1 + n_phi * (n_theta - 3) + 1,
            north_pole_index,
        ]
    )
    tri = np.array(tri)
    quad = np.array(quad)

    return nodes, tri, quad


def tetra_sphere(n):
    corners = np.array(
        [
            [2 * np.sqrt(2) / 3, 0.0, -1.0 / 3.0],
            [-np.sqrt(2) / 3, np.sqrt(2.0 / 3.0), -1.0 / 3.0],
            [-np.sqrt(2) / 3, -np.sqrt(2.0 / 3.0), -1.0 / 3.0],
            [0.0, 0.0, 1.0],
        ]
    )
    # make sure the normals are pointing outwards
    faces = [(0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3)]

    vertices, cells = _compose_from_faces(corners, faces, n)

    # push all nodes to the sphere
    norms = np.sqrt(np.einsum("ij,ij->i", vertices, vertices))
    vertices = (vertices.T / norms).T

    return vertices, cells


def octa_sphere(n: int):
    corners = np.array(
        [
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0],
        ]
    )
    faces = [
        (0, 2, 4),
        (1, 4, 2),
        (1, 3, 4),
        (0, 4, 3),
        (0, 5, 2),
        (1, 2, 5),
        (1, 5, 3),
        (0, 3, 5),
    ]
    vertices, cells = _compose_from_faces(corners, faces, n)

    # push all nodes to the sphere
    norms = np.sqrt(np.einsum("ij,ij->i", vertices, vertices))
    vertices = (vertices.T / norms).T

    return vertices, cells


def icosa_sphere(n: int):
    assert n >= 1
    # Start off with an isosahedron and refine.

    # Construction from
    # <http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html>.
    # Create 12 vertices of a icosahedron.
    t = (1.0 + np.sqrt(5.0)) / 2.0
    corners = np.array(
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

    vertices, cells = _compose_from_faces(corners, faces, n)
    # push all nodes to the sphere
    norms = np.sqrt(np.einsum("ij,ij->i", vertices, vertices))
    vertices = (vertices.T / norms).T

    return vertices, cells
