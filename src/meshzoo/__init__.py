from .__about__ import __version__
from ._ball import ball_hexa, ball_tetra
from ._cube import cube, cube_hexa, cube_tetra
from ._disk import disk, disk_quad
from ._helpers import create_edges, insert_midpoints_edges, plot2d, save2d, show2d
from ._moebius import moebius
from ._ngon import ngon
from ._platonic import icosa_surface
from ._rectangle import rectangle, rectangle_quad, rectangle_tri
from ._sphere import geo_sphere, icosa_sphere, octa_sphere, tetra_sphere, uv_sphere
from ._triangle import triangle
from ._tube import tube

__all__ = [
    "__version__",
    #
    "ball_hexa",
    "ball_tetra",
    "cube",
    "cube_tetra",
    "cube_hexa",
    "disk",
    "disk_quad",
    "moebius",
    "ngon",
    "rectangle",
    "rectangle_tri",
    "rectangle_quad",
    "uv_sphere",
    "icosa_sphere",
    "icosa_surface",
    "octa_sphere",
    "tetra_sphere",
    "geo_sphere",
    "triangle",
    "tube",
    #
    "save2d",
    "show2d",
    "plot2d",
    "create_edges",
    "insert_midpoints_edges",
]
