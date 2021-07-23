import meshzoo


def test_midpoints_edges_tri():
    points, cells = meshzoo.rectangle_tri(a0=(0, 0), a1=(1, 1), n=2)

    assert len(points) == 4
    assert cells.shape == (2, 3)

    points_new, cells_new = meshzoo.insert_midpoints_edges(
        points, cells, cell_type="triangle"
    )

    assert len(points_new) == 9
    assert cells_new.shape == (6, 6)


def test_midpoints_edges_tetra():
    points, cells = meshzoo.cube_tetra(a0=(0, 0, 0), a1=(1, 1, 1), n=2)

    assert len(points) == 8
    assert cells.shape == (5, 4)

    points_new, cells_new = meshzoo.insert_midpoints_edges(
        points, cells, cell_type="tetra"
    )

    assert len(points_new) == 26
    assert cells_new.shape == (5, 10)


def test_midpoints_edges_quad():
    points, cells = meshzoo.rectangle_quad(a0=(0, 0), a1=(1, 1), n=3)

    assert len(points) == 9
    assert cells.shape == (4, 4)

    points_new, cells_new = meshzoo.insert_midpoints_edges(
        points, cells, cell_type="quad"
    )

    assert len(points_new) == 21
    assert cells_new.shape == (8, 8)


def test_midpoints_edges_hexa():
    points, cells = meshzoo.cube_hexa(a0=(0, 0, 0), a1=(1, 1, 1), n=3)

    assert len(points) == 27
    assert cells.shape == (8, 8)

    points_new, cells_new = meshzoo.insert_midpoints_edges(
        points, cells, cell_type="hexahedron"
    )

    assert len(points_new) == 81
    assert cells_new.shape == (8, 20)


if __name__ == "__main__":
    test_midpoints_edges_tetra()
