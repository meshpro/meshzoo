import numpy as np

from ._platonic import icosa_surface, octa_surface, tetra_surface


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
    vertices, cells = tetra_surface(n)
    # push all nodes to the sphere
    norms = np.sqrt(np.einsum("ij,ij->i", vertices, vertices))
    vertices = (vertices.T / norms).T
    return vertices, cells


def octa_sphere(n: int):
    vertices, cells = octa_surface(n)
    # push all nodes to the sphere
    norms = np.sqrt(np.einsum("ij,ij->i", vertices, vertices))
    vertices = (vertices.T / norms).T
    return vertices, cells


def icosa_sphere(n: int, flat_top: bool = False):
    vertices, cells = icosa_surface(n, flat_top)
    # push all nodes to the sphere
    norms = np.sqrt(np.einsum("ij,ij->i", vertices, vertices))
    vertices = (vertices.T / norms).T
    return vertices, cells
