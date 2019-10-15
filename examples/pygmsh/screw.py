import numpy as np

import pygmsh as pg


def create_screw_mesh():

    geom = pg.built_in.Geometry()

    # Draw a cross.
    poly = geom.add_polygon(
        [
            [0.0, 0.5, 0.0],
            [-0.1, 0.1, 0.0],
            [-0.5, 0.0, 0.0],
            [-0.1, -0.1, 0.0],
            [0.0, -0.5, 0.0],
            [0.1, -0.1, 0.0],
            [0.5, 0.0, 0.0],
            [0.1, 0.1, 0.0],
        ],
        lcar=0.05,
    )

    axis = [0, 0, 1]

    geom.extrude(
        poly,
        translation_axis=axis,
        rotation_axis=axis,
        point_on_axis=[0, 0, 0],
        angle=2.0 / 6.0 * np.pi,
    )

    points, cells, _, _, _ = pg.generate_mesh(geom)
    return points, cells["tetra"]


if __name__ == "__main__":
    import meshio

    points, cells = create_screw_mesh()
    meshio.write("screw.vtu", points, {"tetra": cells})
