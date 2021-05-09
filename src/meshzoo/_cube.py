from typing import Tuple, Union

import numpy as np


# backwards compatibility
def cube(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    z0: float,
    z1: float,
    nx: int,
    ny: int,
    nz: int,
):
    return cube_tetra((x0, y0, z0), (x1, y1, z1), (nx, ny, nz))


def cube_hexa(
    a0: Tuple[float, float, float],
    a1: Tuple[float, float, float],
    n: Union[int, Tuple[int, int, int]],
):
    if isinstance(n, tuple):
        assert len(n) == 3
    else:
        n = (n, n, n)

    xmin, ymin, zmin = a0
    xmax, ymax, zmax = a1
    nx, ny, nz = n

    # Generate suitable ranges for parametrization
    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)
    z_range = np.linspace(zmin, zmax, nz)

    # Create the vertices.
    x, y, z = np.meshgrid(x_range, y_range, z_range, indexing="ij")
    # Alternative with slightly different order:
    # ```
    # nodes = np.stack([x, y, z]).T.reshape(-1, 3)
    # ```
    nodes = np.array([x, y, z]).T.reshape(-1, 3)

    # Create the elements (cells).
    a0 = np.add.outer(np.array(range(nx - 1)), nx * np.array(range(ny - 1)))
    a = np.add.outer(a0, nx * ny * np.array(range(nz - 1)))
    elems = np.concatenate(
        [
            a[..., None],
            a[..., None] + 1,
            a[..., None] + nx + 1,
            a[..., None] + nx,
            #
            a[..., None] + nx * ny,
            a[..., None] + nx * ny + 1,
            a[..., None] + nx * ny + nx + 1,
            a[..., None] + nx * ny + nx,
        ],
        axis=3,
    ).reshape(-1, 8)

    return nodes, elems


def cube_tetra(
    a0: Tuple[float, float, float],
    a1: Tuple[float, float, float],
    n: Union[int, Tuple[int, int, int]],
):
    """Canonical tetrahedrization of the cube.
    Input:
    Edge lenghts of the cube
    Number of nodes along the edges.
    """
    if isinstance(n, tuple):
        assert len(n) == 3
    else:
        n = (n, n, n)

    xmin, ymin, zmin = a0
    xmax, ymax, zmax = a1
    nx, ny, nz = n

    # Generate suitable ranges for parametrization
    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)
    z_range = np.linspace(zmin, zmax, nz)

    # Create the vertices.
    x, y, z = np.meshgrid(x_range, y_range, z_range, indexing="ij")
    # Alternative with slightly different order:
    # ```
    # nodes = np.stack([x, y, z]).T.reshape(-1, 3)
    # ```
    nodes = np.array([x, y, z]).T.reshape(-1, 3)

    # Create the elements (cells).
    # There is 1 way to split a cube into 5 tetrahedra,
    # and 12 ways to split it into 6 tetrahedra.
    # See
    # <http://www.baumanneduard.ch/Splitting%20a%20cube%20in%20tetrahedras2.htm>
    # Also interesting: <http://en.wikipedia.org/wiki/Marching_tetrahedrons>.

    a0 = np.add.outer(np.array(range(nx - 1)), nx * np.array(range(ny - 1)))
    a = np.add.outer(a0, nx * ny * np.array(range(nz - 1)))

    # The general scheme here is:
    #  * Initialize everything with `a`, equivalent to
    #    [i + nx * j + nx*ny * k].
    #  * Add the "even" elements.
    #  * Switch the element styles for every other element to make sure the
    #    edges match at the faces of the cubes.
    # The last step requires adapting the original pattern at
    #     [1::2, 0::2, 0::2, :]
    #     [0::2, 1::2, 0::2, :]
    #     [0::2, 0::2, 1::2, :]
    #     [1::2, 1::2, 1::2, :]
    #

    # Tetrahedron 0:
    # [
    # i   + nx*j     + nx*ny * k,
    # i   + nx*(j+1) + nx*ny * k,
    # i+1 + nx*j     + nx*ny * k,
    # i   + nx*j     + nx*ny * (k+1)
    # ]
    # TODO get
    # ```
    # elems0 = np.stack([a, a + nx, a + 1, a + nx*ny]).T
    # ```
    # back.
    elems0 = np.concatenate(
        [a[..., None], a[..., None] + nx, a[..., None] + 1, a[..., None] + nx * ny],
        axis=3,
    )

    # Every other element cube:
    # [
    # i+1 + nx * j     + nx*ny * k,
    # i+1 + nx * (j+1) + nx*ny * k,
    # i   + nx * j     + nx*ny * k,
    # i+1 + nx * j     + nx*ny * (k+1)
    # ]
    elems0[1::2, 0::2, 0::2, 0] += 1
    elems0[0::2, 1::2, 0::2, 0] += 1
    elems0[0::2, 0::2, 1::2, 0] += 1
    elems0[1::2, 1::2, 1::2, 0] += 1

    elems0[1::2, 0::2, 0::2, 1] += 1
    elems0[0::2, 1::2, 0::2, 1] += 1
    elems0[0::2, 0::2, 1::2, 1] += 1
    elems0[1::2, 1::2, 1::2, 1] += 1

    elems0[1::2, 0::2, 0::2, 2] -= 1
    elems0[0::2, 1::2, 0::2, 2] -= 1
    elems0[0::2, 0::2, 1::2, 2] -= 1
    elems0[1::2, 1::2, 1::2, 2] -= 1

    elems0[1::2, 0::2, 0::2, 3] += 1
    elems0[0::2, 1::2, 0::2, 3] += 1
    elems0[0::2, 0::2, 1::2, 3] += 1
    elems0[1::2, 1::2, 1::2, 3] += 1

    # Tetrahedron 1:
    # [
    # i   + nx*(j+1) + nx*ny * k,
    # i+1 + nx*(j+1) + nx*ny * k,
    # i+1 + nx*j     + nx*ny * k,
    # i+1 + nx*(j+1) + nx*ny * (k+1)
    # ]
    # elems1 = np.stack([a + nx, a + 1 + nx, a + 1, a + 1 + nx + nx*ny]).T
    elems1 = np.concatenate(
        [
            a[..., None] + nx,
            a[..., None] + 1 + nx,
            a[..., None] + 1,
            a[..., None] + 1 + nx + nx * ny,
        ],
        axis=3,
    )

    # Every other element cube:
    # [
    # i+1 + nx * (j+1) + nx*ny * k,
    # i   + nx * (j+1) + nx*ny * k,
    # i   + nx * j     + nx*ny * k,
    # i   + nx * (j+1) + nx*ny * (k+1)
    # ]
    elems1[1::2, 0::2, 0::2, 0] += 1
    elems1[0::2, 1::2, 0::2, 0] += 1
    elems1[0::2, 0::2, 1::2, 0] += 1
    elems1[1::2, 1::2, 1::2, 0] += 1

    elems1[1::2, 0::2, 0::2, 1] -= 1
    elems1[0::2, 1::2, 0::2, 1] -= 1
    elems1[0::2, 0::2, 1::2, 1] -= 1
    elems1[1::2, 1::2, 1::2, 1] -= 1

    elems1[1::2, 0::2, 0::2, 2] -= 1
    elems1[0::2, 1::2, 0::2, 2] -= 1
    elems1[0::2, 0::2, 1::2, 2] -= 1
    elems1[1::2, 1::2, 1::2, 2] -= 1

    elems1[1::2, 0::2, 0::2, 3] -= 1
    elems1[0::2, 1::2, 0::2, 3] -= 1
    elems1[0::2, 0::2, 1::2, 3] -= 1
    elems1[1::2, 1::2, 1::2, 3] -= 1

    # Tetrahedron 2:
    # [
    # i   + nx*(j+1) + nx*ny * k,
    # i+1 + nx*j     + nx*ny * k,
    # i   + nx*j     + nx*ny * (k+1),
    # i+1 + nx*(j+1) + nx*ny * (k+1)
    # ]
    # elems2 = np.stack([a + nx, a + 1, a + nx*ny, a + 1 + nx + nx*ny]).T
    elems2 = np.concatenate(
        [
            a[..., None] + nx,
            a[..., None] + 1,
            a[..., None] + nx * ny,
            a[..., None] + 1 + nx + nx * ny,
        ],
        axis=3,
    )

    # Every other element cube:
    # [
    # i+1 + nx * (j+1) + nx*ny * k,
    # i   + nx * j     + nx*ny * k,
    # i+1 + nx * j     + nx*ny * (k+1),
    # i   + nx * (j+1) + nx*ny * (k+1)
    # ]
    elems2[1::2, 0::2, 0::2, 0] += 1
    elems2[0::2, 1::2, 0::2, 0] += 1
    elems2[0::2, 0::2, 1::2, 0] += 1
    elems2[1::2, 1::2, 1::2, 0] += 1

    elems2[1::2, 0::2, 0::2, 1] -= 1
    elems2[0::2, 1::2, 0::2, 1] -= 1
    elems2[0::2, 0::2, 1::2, 1] -= 1
    elems2[1::2, 1::2, 1::2, 1] -= 1

    elems2[1::2, 0::2, 0::2, 2] += 1
    elems2[0::2, 1::2, 0::2, 2] += 1
    elems2[0::2, 0::2, 1::2, 2] += 1
    elems2[1::2, 1::2, 1::2, 2] += 1

    elems2[1::2, 0::2, 0::2, 3] -= 1
    elems2[0::2, 1::2, 0::2, 3] -= 1
    elems2[0::2, 0::2, 1::2, 3] -= 1
    elems2[1::2, 1::2, 1::2, 3] -= 1

    # Tetrahedron 3:
    # [
    # i   + nx * (j+1) + nx*ny * k,
    # i   + nx * j     + nx*ny * (k+1),
    # i   + nx * (j+1) + nx*ny * (k+1),
    # i+1 + nx * (j+1) + nx*ny * (k+1)
    # ]
    # elems3 = np.stack([
    #     a + nx,
    #     a + nx*ny,
    #     a + nx + nx*ny,
    #     a + 1 + nx + nx*ny
    #     ]).T
    elems3 = np.concatenate(
        [
            a[..., None] + nx,
            a[..., None] + nx * ny,
            a[..., None] + nx + nx * ny,
            a[..., None] + 1 + nx + nx * ny,
        ],
        axis=3,
    )

    # Every other element cube:
    # [
    # i+1 + nx * (j+1) + nx*ny * k,
    # i+1 + nx * j     + nx*ny * (k+1),
    # i+1 + nx * (j+1) + nx*ny * (k+1),
    # i   + nx * (j+1) + nx*ny * (k+1)
    # ]
    elems3[1::2, 0::2, 0::2, 0] += 1
    elems3[0::2, 1::2, 0::2, 0] += 1
    elems3[0::2, 0::2, 1::2, 0] += 1
    elems3[1::2, 1::2, 1::2, 0] += 1

    elems3[1::2, 0::2, 0::2, 1] += 1
    elems3[0::2, 1::2, 0::2, 1] += 1
    elems3[0::2, 0::2, 1::2, 1] += 1
    elems3[1::2, 1::2, 1::2, 1] += 1

    elems3[1::2, 0::2, 0::2, 2] += 1
    elems3[0::2, 1::2, 0::2, 2] += 1
    elems3[0::2, 0::2, 1::2, 2] += 1
    elems3[1::2, 1::2, 1::2, 2] += 1

    elems3[1::2, 0::2, 0::2, 3] -= 1
    elems3[0::2, 1::2, 0::2, 3] -= 1
    elems3[0::2, 0::2, 1::2, 3] -= 1
    elems3[1::2, 1::2, 1::2, 3] -= 1

    # Tetrahedron 4:
    # [
    # i+1 + nx * j     + nx*ny * k,
    # i   + nx * j     + nx*ny * (k+1),
    # i+1 + nx * (j+1) + nx*ny * (k+1),
    # i+1 + nx * j     + nx*ny * (k+1)
    # ]
    # elems4 = np.stack([
    #     a + 1,
    #     a + nx*ny,
    #     a + 1 + nx + nx*ny,
    #     a + 1 + nx*ny
    #     ]).T
    elems4 = np.concatenate(
        [
            a[..., None] + 1,
            a[..., None] + nx * ny,
            a[..., None] + 1 + nx + nx * ny,
            a[..., None] + 1 + nx * ny,
        ],
        axis=3,
    )

    # Every other element cube:
    # [
    # i   + nx * j     + nx*ny * k,
    # i+1 + nx * j     + nx*ny * (k+1),
    # i   + nx * (j+1) + nx*ny * (k+1),
    # i   + nx * j     + nx*ny * (k+1)
    # ]
    elems4[1::2, 0::2, 0::2, 0] -= 1
    elems4[0::2, 1::2, 0::2, 0] -= 1
    elems4[0::2, 0::2, 1::2, 0] -= 1
    elems4[1::2, 1::2, 1::2, 0] -= 1

    elems4[1::2, 0::2, 0::2, 1] += 1
    elems4[0::2, 1::2, 0::2, 1] += 1
    elems4[0::2, 0::2, 1::2, 1] += 1
    elems4[1::2, 1::2, 1::2, 1] += 1

    elems4[1::2, 0::2, 0::2, 2] -= 1
    elems4[0::2, 1::2, 0::2, 2] -= 1
    elems4[0::2, 0::2, 1::2, 2] -= 1
    elems4[1::2, 1::2, 1::2, 2] -= 1

    elems4[1::2, 0::2, 0::2, 3] -= 1
    elems4[0::2, 1::2, 0::2, 3] -= 1
    elems4[0::2, 0::2, 1::2, 3] -= 1
    elems4[1::2, 1::2, 1::2, 3] -= 1

    elems = np.vstack(
        [
            elems0.reshape(-1, 4),
            elems1.reshape(-1, 4),
            elems2.reshape(-1, 4),
            elems3.reshape(-1, 4),
            elems4.reshape(-1, 4),
        ]
    )

    return nodes, elems
