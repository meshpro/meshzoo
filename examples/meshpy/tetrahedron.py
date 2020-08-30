#!/usr/bin/env python
"""
Create irregular mesh on a regular tetrahedron centered at the origin.
"""
import meshpy.tet
import numpy as np


def create_tetrahedron_mesh(maxvol=0.1):
    # circumcircle radius
    r = 5.0

    # boundary points
    points = []
    points.append((0.0, 0.0, r))
    # theta = arccos(-1/3) (tetrahedral angle)
    costheta = -1.0 / 3.0
    sintheta = 2.0 / 3.0 * np.sqrt(2.0)
    # phi = 0.0
    sinphi = 0.0
    cosphi = 1.0
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))
    # phi = np.pi * 2.0 / 3.0
    sinphi = np.sqrt(3.0) / 2.0
    cosphi = -0.5
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))
    # phi = - np.pi * 2.0 / 3.0
    sinphi = -np.sqrt(3.0) / 2.0
    cosphi = -0.5
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))

    # boundary faces
    facets = [[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 2, 3]]

    # create the mesh
    # Set the geometry and build the mesh.
    info = meshpy.tet.MeshInfo()
    info.set_points(points)
    info.set_facets(facets)
    meshpy_mesh = meshpy.tet.build(info, max_volume=maxvol)

    return np.array(meshpy_mesh.points), np.array(meshpy_mesh.elements)


if __name__ == "__main__":
    import meshio

    points, cells = create_tetrahedron_mesh(10.0)
    meshio.write("tetrahedron.vtu", points, {"tetra": cells})
