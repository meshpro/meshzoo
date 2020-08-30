"""Creates meshes on a 3D L-shape.
"""
import meshpy.tet
import numpy as np


def create_mesh(maxvol):
    # circumcirlce radius
    cc_radius = 10.0
    lx = 2.0 / np.sqrt(3.0) * cc_radius
    ly = lx
    lz = lx

    # create the mesh data structure
    # Corner points of the cube
    points = [
        (-0.5 * lx, -0.5 * ly, -0.5 * lz),
        (0.5 * lx, -0.5 * ly, -0.5 * lz),
        (0.5 * lx, 0.5 * ly, -0.5 * lz),
        (-0.5 * lx, 0.5 * ly, -0.5 * lz),
        (-0.5 * lx, -0.5 * ly, 0.5 * lz),
        (0.5 * lx, 0.5 * ly, 0.5 * lz),
        (-0.5 * lx, 0.5 * ly, 0.5 * lz),
        (0.0, -0.5 * ly, 0.5 * lz),
        (0.0, -0.5 * ly, 0.0),
        (0.5 * lx, -0.5 * ly, 0.0),
        (0.5 * lx, 0.0, 0.0),
        (0.5 * lx, 0.0, 0.5 * lz),
        (0.0, 0.0, 0.5 * lz),
        (0.0, 0.0, 0.0),
    ]
    facets = [
        [0, 1, 2, 3],
        [4, 7, 12, 11, 5, 6],
        [0, 1, 9, 8, 7, 4],
        [1, 2, 5, 11, 10, 9],
        [2, 5, 6, 3],
        [3, 6, 4, 0],
        [8, 13, 12, 7],
        [8, 9, 10, 13],
        [10, 11, 12, 13],
    ]
    # create the mesh
    # Set the geometry and build the mesh.
    info = meshpy.tet.MeshInfo()
    info.set_points(points)
    info.set_facets(facets)
    meshpy_mesh = meshpy.tet.build(info, max_volume=maxvol)

    return np.array(meshpy_mesh.points), np.array(meshpy_mesh.elements)


if __name__ == "__main__":
    import meshio

    points, cells = create_mesh(0.1)
    meshio.write("lshape3d.e", points, {"tetra": cells})
