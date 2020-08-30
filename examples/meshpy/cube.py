"""
Creates meshes on a cube.
"""
import meshpy.tet
import numpy as np


def create_mesh(maxvol):
    # get the file name to be written to

    # circumcirlce radius
    cc_radius = 5.0
    lx = 2.0 / np.sqrt(3.0) * cc_radius
    ly = lx
    lz = lx

    # Corner points of the cube
    points = [
        (-0.5 * lx, -0.5 * ly, -0.5 * lz),
        (0.5 * lx, -0.5 * ly, -0.5 * lz),
        (0.5 * lx, 0.5 * ly, -0.5 * lz),
        (-0.5 * lx, 0.5 * ly, -0.5 * lz),
        (-0.5 * lx, -0.5 * ly, 0.5 * lz),
        (0.5 * lx, -0.5 * ly, 0.5 * lz),
        (0.5 * lx, 0.5 * ly, 0.5 * lz),
        (-0.5 * lx, 0.5 * ly, 0.5 * lz),
    ]
    facets = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 4, 5, 1],
        [1, 5, 6, 2],
        [2, 6, 7, 3],
        [3, 7, 4, 0],
    ]

    # create the mesh
    info = meshpy.tet.MeshInfo()
    info.set_points(points)
    info.set_facets(facets)
    meshpy_mesh = meshpy.tet.build(info, max_volume=maxvol)

    return np.array(meshpy_mesh.points), np.array(meshpy_mesh.elements)


if __name__ == "__main__":
    import meshio

    points, cells = create_mesh(0.1)
    meshio.write("cube.e", points, {"tetra": cells})
