import pytest

import meshzoo


def test_midpoints_edges_wrongtype():
    points, cells = meshzoo.rectangle_tri(a0=(0, 0), a1=(1, 1), n=2)

    with pytest.raises(TypeError):
        points_new, cells_new = meshzoo.insert_midpoints_edges(
            points, cells, cell_type="unknown"
        )


def test_midpoints_faces_wrongtype():
    points, cells = meshzoo.rectangle_tri(a0=(0, 0), a1=(1, 1), n=2)

    with pytest.raises(TypeError):
        points_new, cells_new = meshzoo.insert_midpoints_faces(
            points, cells, cell_type="unknown"
        )


def test_midpoints_volumes_wrongtype():
    points, cells = meshzoo.rectangle_tri(a0=(0, 0), a1=(1, 1), n=2)

    with pytest.raises(TypeError):
        points_new, cells_new = meshzoo.insert_midpoints_faces(
            points, cells, cell_type="unknown"
        )


def test_midpoints_edges_tri():
    points, cells = meshzoo.rectangle_tri(a0=(0, 0), a1=(1, 1), n=2)

    assert len(points) == 4
    assert cells.shape == (2, 3)

    points_new, cells_new = meshzoo.insert_midpoints_edges(
        points, cells, cell_type="triangle"
    )

    assert len(points_new) == 9
    assert cells_new.shape == (2, 6)


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
    assert cells_new.shape == (4, 8)


def test_midpoints_edges_hexa():
    points, cells = meshzoo.cube_hexa(a0=(0, 0, 0), a1=(1, 1, 1), n=3)

    assert len(points) == 27
    assert cells.shape == (8, 8)

    points_new, cells_new = meshzoo.insert_midpoints_edges(
        points, cells, cell_type="hexahedron"
    )

    assert len(points_new) == 81
    assert cells_new.shape == (8, 20)


def test_midpoints_faces_tri():
    points, cells = meshzoo.rectangle_tri(a0=(0, 0), a1=(1, 1), n=2)

    assert len(points) == 4
    assert cells.shape == (2, 3)

    points_new, cells_new = meshzoo.insert_midpoints_faces(
        points, cells, cell_type="triangle"
    )

    assert len(points_new) == 6
    assert cells_new.shape == (2, 4)


def test_midpoints_faces_tetra():
    points, cells = meshzoo.cube_tetra(a0=(0, 0, 0), a1=(1, 1, 1), n=2)

    assert len(points) == 8
    assert cells.shape == (5, 4)

    points_new, cells_new = meshzoo.insert_midpoints_faces(
        points, cells, cell_type="tetra"
    )

    assert len(points_new) == 24
    assert cells_new.shape == (5, 8)


def test_midpoints_faces_quad():
    points, cells = meshzoo.rectangle_quad(a0=(0, 0), a1=(1, 1), n=3)

    assert len(points) == 9
    assert cells.shape == (4, 4)

    points_new, cells_new = meshzoo.insert_midpoints_faces(
        points, cells, cell_type="quad"
    )

    assert len(points_new) == 13
    assert cells_new.shape == (4, 5)


def test_midpoints_faces_hexa():
    points, cells = meshzoo.cube_hexa(a0=(0, 0, 0), a1=(1, 1, 1), n=3)

    assert len(points) == 27
    assert cells.shape == (8, 8)

    points_new, cells_new = meshzoo.insert_midpoints_faces(
        points, cells, cell_type="hexahedron"
    )

    assert len(points_new) == 63
    assert cells_new.shape == (8, 14)


def test_midpoints_volumes_tri():
    points, cells = meshzoo.rectangle_tri(a0=(0, 0), a1=(1, 1), n=2)

    assert len(points) == 4
    assert cells.shape == (2, 3)

    with pytest.raises(TypeError):
        points_new, cells_new = meshzoo.insert_midpoints_volumes(
            points, cells, cell_type="triangle"
        )


def test_midpoints_volumes_tetra():
    points, cells = meshzoo.cube_tetra(a0=(0, 0, 0), a1=(1, 1, 1), n=2)

    assert len(points) == 8
    assert cells.shape == (5, 4)

    points_new, cells_new = meshzoo.insert_midpoints_volumes(
        points, cells, cell_type="tetra"
    )

    assert len(points_new) == 13
    assert cells_new.shape == (5, 5)


def test_midpoints_volumes_quad():
    points, cells = meshzoo.rectangle_quad(a0=(0, 0), a1=(1, 1), n=3)

    assert len(points) == 9
    assert cells.shape == (4, 4)

    with pytest.raises(TypeError):
        points_new, cells_new = meshzoo.insert_midpoints_volumes(
            points, cells, cell_type="quad"
        )


def test_midpoints_volumes_hexa():
    points, cells = meshzoo.cube_hexa(a0=(0, 0, 0), a1=(1, 1, 1), n=3)

    assert len(points) == 27
    assert cells.shape == (8, 8)

    points_new, cells_new = meshzoo.insert_midpoints_volumes(
        points, cells, cell_type="hexahedron"
    )

    assert len(points_new) == 35
    assert cells_new.shape == (8, 9)


if __name__ == "__main__":
    test_midpoints_edges_wrongtype()
    test_midpoints_edges_tri()
    test_midpoints_edges_tetra()
    test_midpoints_edges_quad()
    test_midpoints_edges_hexa()

    test_midpoints_faces_wrongtype()
    test_midpoints_faces_tri()
    test_midpoints_faces_tetra()
    test_midpoints_faces_quad()
    test_midpoints_faces_hexa()

    test_midpoints_volumes_wrongtype()
    test_midpoints_volumes_tri()
    test_midpoints_volumes_tetra()
    test_midpoints_volumes_quad()
    test_midpoints_volumes_hexa()
