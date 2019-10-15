import dolfin

import mshr


def create_toy_mesh():

    box = mshr.Box(dolfin.Point(-3, -1, -0.5), dolfin.Point(3, 1, 0.5))

    c1 = mshr.Cylinder(dolfin.Point(0, 0, -2), dolfin.Point(0, 0, 2), 0.6, 0.6)
    b1 = mshr.Box(dolfin.Point(-2.5, -0.5, -2), dolfin.Point(-1.5, 0.5, 2))

    # "triangle"
    t1 = mshr.Polygon(
        [
            dolfin.Point(2.5, -0.5, 0),
            dolfin.Point(2.5, 0.5, 0),
            dolfin.Point(1.5, -0.5, 0),
        ]
    )
    g3d = mshr.Extrude2D(t1, -2)
    g3d = mshr.CSGTranslation(g3d, dolfin.Point(0, 0, 1))

    m = mshr.generate_mesh(box - c1 - b1 - g3d, 40, "cgal")

    return m.coordinates(), m.cells()


if __name__ == "__main__":
    import meshio

    points, cells = create_toy_mesh()
    meshio.write("toy.e", points, {"tetra": cells})
