import numpy as np
from meshpy.geometry import EXT_OPEN, GeometryBuilder, generate_surface_of_revolution
from meshpy.tet import MeshInfo, build


def create_ball_mesh(num_longi_points=10):

    radius = 5.0

    radial_subdiv = 2 * num_longi_points

    dphi = np.pi / num_longi_points

    # Make sure the nodes meet at the poles of the ball.
    def truncate(r):
        if abs(r) < 1e-10:
            return 0
        else:
            return r

    # Compute the volume of a canonical tetrahedron
    # with edgelength radius*dphi.
    a = radius * dphi
    canonical_tet_volume = np.sqrt(2.0) / 12 * a**3

    # Build outline for surface of revolution.
    rz = [
        (truncate(radius * np.sin(i * dphi)), radius * np.cos(i * dphi))
        for i in range(num_longi_points + 1)
    ]

    geob = GeometryBuilder()
    geob.add_geometry(
        *generate_surface_of_revolution(
            rz, closure=EXT_OPEN, radial_subdiv=radial_subdiv
        )
    )
    mesh_info = MeshInfo()
    geob.set(mesh_info)
    meshpy_mesh = build(mesh_info, max_volume=canonical_tet_volume)

    return np.array(meshpy_mesh.points), np.array(meshpy_mesh.elements)


if __name__ == "__main__":
    import meshio

    points, cells = create_ball_mesh()
    meshio.write("ball.e", points, {"tetra": cells})
