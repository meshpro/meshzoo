# meshzoo

[![PyPi Version](https://img.shields.io/pypi/v/meshzoo.svg?style=flat-square)](https://pypi.org/project/meshzoo/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/meshzoo.svg?style=flat-square)](https://pypi.org/project/meshzoo/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/meshzoo.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/meshzoo)
[![Downloads](https://pepy.tech/badge/meshzoo/month?style=flat-square)](https://pepy.tech/project/meshzoo)

<!--[![PyPi downloads](https://img.shields.io/pypi/dm/meshzoo.svg?style=flat-square)](https://pypistats.org/packages/meshzoo)-->

[![Discord](https://img.shields.io/static/v1?logo=discord&logoColor=white&label=chat&message=on%20discord&color=7289da&style=flat-square)](https://discord.gg/PBCCvwHqpv)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/meshzoo/ci?style=flat-square)](https://github.com/nschloe/meshzoo/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/meshzoo.svg?style=flat-square)](https://codecov.io/gh/nschloe/meshzoo)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/meshzoo.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/meshzoo)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

When generating meshes for FEM/FVM computations, sometimes your geometry is so simple
that you don't need a complex mesh generator (like
[pygmsh](https://github.com/nschloe/pygmsh/),
[MeshPy](https://github.com/inducer/meshpy),
[mshr](https://bitbucket.org/fenics-project/mshr),
[pygalmesh](https://github.com/nschloe/pygalmesh/),
[dmsh](https://github.com/nschloe/dmsh/)),
but something simple and fast that makes use of the structure of the domain. Enter
meshzoo.

### Examples

#### Triangle

<img src="https://nschloe.github.io/meshzoo/triangle.svg" width="20%">

```python
import meshzoo

bary, cells = meshzoo.triangle(8)

# corners = numpy.array(
#     [
#         [0.0, -0.5 * numpy.sqrt(3.0), +0.5 * numpy.sqrt(3.0)],
#         [1.0, -0.5, -0.5],
#     ]
# )
# points = numpy.dot(corners, bary).T

# Process the mesh, e.g., write it to a file using meshio
# meshio.write_points_cells("triangle.vtk", points, {"triangle": cells})
```

#### Rectangle

<table width="100%">
  <tr width="100%">
  <td width="50%"><img src="https://nschloe.github.io/meshzoo/rectangle.svg"/></td>
  <td width="50%"><img src="https://nschloe.github.io/meshzoo/rectangle-quad.svg"/></td>
  </tr>
</table>

```python
import meshzoo
import numpy as np

points, cells = meshzoo.rectangle_tri(
    np.linspace(0.0, 1.0, 11),
    np.linspace(0.0, 1.0, 11),
    variant="zigzag",  # or "up", "down", "center"
)

points, cells = meshzoo.rectangle_quad(
    np.linspace(0.0, 1.0, 11),
    np.linspace(0.0, 1.0, 11),
    cell_type="quad4",  # or "quad8", "quad9"
)
```

#### Regular polygon

| <img src="https://nschloe.github.io/meshzoo/4gon.svg" width="70%"> | <img src="https://nschloe.github.io/meshzoo/6gon.svg" width="70%"> | <img src="https://nschloe.github.io/meshzoo/9gon.svg" width="70%"> |
| :----------------------------------------------------------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------: |
|                        `meshzoo.ngon(4, 8)`                        |                        `meshzoo.ngon(6, 8)`                        |                        `meshzoo.ngon(9, 8)`                        |

```python
import meshzoo

points, cells = meshzoo.ngon(5, 11)
```

#### Disk

| <img src="https://nschloe.github.io/meshzoo/4gon_disk.svg" width="70%"> | <img src="https://nschloe.github.io/meshzoo/6gon_disk.svg" width="70%"> | <img src="https://nschloe.github.io/meshzoo/9gon_disk.svg" width="70%"> |
| :---------------------------------------------------------------------: | :---------------------------------------------------------------------: | :---------------------------------------------------------------------: |
|                          `meshzoo.disk(4, 8)`                           |                          `meshzoo.disk(6, 8)`                           |                          `meshzoo.disk(9, 8)`                           |

The disk meshes are inflations of regular polygons.

```python
import meshzoo

points, cells = meshzoo.disk(6, 11)

points, cells = meshzoo.disk_quad(10, cell_type="quad4")  # or "quad8", "quad9"
```

#### Möbius strip

<img src="https://nschloe.github.io/meshzoo/moebius.png" width="20%">

```python
import meshzoo

points, cells = meshzoo.moebius(num_twists=1, nl=60, nw=11)
```

#### Sphere (surface)

| <img src="https://nschloe.github.io/meshzoo/uv_sphere.png" width="80%"> | <img src="https://nschloe.github.io/meshzoo/geo-sphere.png" width="60%"> |
| :---------------------------------------------------------------------: | :----------------------------------------------------------------------: |

```python
import meshzoo

points, cells = meshzoo.uv_sphere(num_points_per_circle=20, num_circles=10, radius=1.0)
points, tri, quad = meshzoo.geo_sphere(
    num_points_per_circle=20, num_circles=10, radius=1.0
)
```

Spheres can also be generated by refining the faces of [platonic
solids](https://en.wikipedia.org/wiki/Platonic_solid) and then "inflating" them. meshzoo
implements a few of them. The sphere generated from the icosahedron has the
highest-quality (most equilateral) triangles.

All cells are oriented such that its normals point outwards.

| <img src="https://nschloe.github.io/meshzoo/tetra-sphere.png" width="70%"> | <img src="https://nschloe.github.io/meshzoo/octa-sphere.png" width="70%"> | <img src="https://nschloe.github.io/meshzoo/icosa-sphere.png" width="70%"> |
| :------------------------------------------------------------------------: | :-----------------------------------------------------------------------: | :------------------------------------------------------------------------: |
|                         `meshzoo.tetra_sphere(10)`                         |                         `meshzoo.octa_sphere(10)`                         |                         `meshzoo.icosa_sphere(10)`                         |

#### Ball (solid)

| <img src="https://nschloe.github.io/meshzoo/ball-tetra.png" width="70%"> | <img src="https://nschloe.github.io/meshzoo/ball-hexa.png" width="70%"> |
| :----------------------------------------------------------------------: | :---------------------------------------------------------------------: |

```python
import meshzoo

points, cells = meshzoo.ball_tetra(10)
points, cells = meshzoo.ball_hexa(10)
```

#### Tube

<img src="https://nschloe.github.io/meshzoo/tube.png" width="20%">

```python
import meshzoo

points, cells = meshzoo.tube(length=1.0, radius=1.0, n=30)
```

#### Cube

| <img src="https://nschloe.github.io/meshzoo/cube.png" width="70%"> | <img src="https://nschloe.github.io/meshzoo/cube-hexa.png" width="50%"> |
| :----------------------------------------------------------------: | :---------------------------------------------------------------------: |

```python
import meshzoo
import numpy as np

points, cells = meshzoo.cube_tetra(
    np.linspace(0.0, 1.0, 11), np.linspace(0.0, 1.0, 11), np.linspace(0.0, 1.0, 11)
)
points, cells = meshzoo.cube_hexa(
    np.linspace(0.0, 1.0, 11), np.linspace(0.0, 1.0, 11), np.linspace(0.0, 1.0, 11)
)
```

### Extra, extra

In addition to this, the
[`examples/`](https://github.com/nschloe/meshzoo/tree/main/examples) directory
contains a couple of instructive examples for other mesh generators.

### Installation

meshzoo is [available from the Python Package
Index](https://pypi.org/project/meshzoo/), so simply do

```
pip install meshzoo
```

to install.

### Testing

To run the meshzoo unit tests, check out this repository and run

```
pytest
```

### License

This software is published under the [GPLv3
license](https://www.gnu.org/licenses/gpl-3.0.en.html).
