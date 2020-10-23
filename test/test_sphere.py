import numpy
from helpers import _near_equal

import meshzoo


def test_uv_sphere(num_points_per_circle=20, num_circles=10):
    points, cells = meshzoo.uv_sphere(num_points_per_circle, num_circles)
    assert len(points) == 162
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 320
    # make sure that the cell normals points outwards
    pc = points[cells]
    midpoints = numpy.sum(pc, axis=1) / 3.0
    nrm = numpy.sqrt(numpy.einsum("ij,ij->i", midpoints, midpoints))
    normals = (midpoints.T / nrm).T
    cross = numpy.cross(
        pc[:, 1, :] - pc[:, 0, :],
        pc[:, 2, :] - pc[:, 0, :],
    )
    normals_dir = numpy.einsum("ij,ij->i", normals, cross)

    import meshio

    meshio.write_points_cells(
        "out.vtk",
        points,
        {"triangle": cells},
        point_data={"idx": numpy.arange(len(points))},
        cell_data={"normals": [normals_dir]},
    )

    assert (normals_dir > 0.0).all()


def test_icosa_sphere(n=16):
    points, cells = meshzoo.icosa_sphere(n)
    # import meshio
    # meshio.write_points_cells("out.vtk", points, {"triangle": cells})
    assert len(points) == 2562
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 5120


def test_octa_sphere(n=16):
    points, cells = meshzoo.octa_sphere(n)
    # import meshio
    # meshio.write_points_cells("out.vtk", points, {"triangle": cells})
    assert len(points) == 1026
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 2048


def test_tetra_sphere(n=16):
    points, cells = meshzoo.tetra_sphere(n)
    # import meshio
    # meshio.write_points_cells("out.vtk", points, {"triangle": cells})
    assert len(points) == 514
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 1024


if __name__ == "__main__":
    test_uv_sphere(20, 10)
