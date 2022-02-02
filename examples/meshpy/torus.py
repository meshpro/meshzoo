#!/usr/bin/env python

import numpy as np
from meshpy.geometry import (
    EXT_CLOSED_IN_RZ,
    GeometryBuilder,
    generate_surface_of_revolution,
)
from meshpy.tet import MeshInfo, build


def create_mesh(big_r=1.0, small_r=0.5, num_points=10):
    dphi = 2 * np.pi / num_points

    # Compute the volume of a canonical tetrahedron
    # with edgelength radius2*dphi.
    a = small_r * dphi
    canonical_tet_volume = np.sqrt(2.0) / 12 * a**3

    radial_subdiv = int(2 * np.pi * big_r / a)

    rz = [
        (big_r + small_r * np.cos(i * dphi), 0.5 * small_r * np.sin(i * dphi))
        for i in range(num_points)
    ]

    geob = GeometryBuilder()
    geob.add_geometry(
        *generate_surface_of_revolution(
            rz, closure=EXT_CLOSED_IN_RZ, radial_subdiv=radial_subdiv
        )
    )
    mesh_info = MeshInfo()
    geob.set(mesh_info)
    meshpy_mesh = build(mesh_info, max_volume=canonical_tet_volume)

    return np.array(meshpy_mesh.points), np.array(meshpy_mesh.elements)


if __name__ == "__main__":
    import meshio

    points, cells = create_mesh()
    meshio.write("torus.e", points, {"tetra": cells})
