<p align="center">
  <a href="https://github.com/meshpro/meshzoo"><img alt="meshzoo" src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/meshzoo-logo.svg" width="60%"></a>
</p>

[![PyPi Version](https://img.shields.io/pypi/v/meshzoo.svg?style=flat-square)](https://pypi.org/project/meshzoo/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/meshzoo.svg?style=flat-square)](https://pypi.org/project/meshzoo/)
[![GitHub stars](https://img.shields.io/github/stars/meshpro/meshzoo.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/meshpro/meshzoo)
[![Downloads](https://pepy.tech/badge/meshzoo/month?style=flat-square)](https://pepy.tech/project/meshzoo)

When generating meshes for FEM/FVM computations, sometimes your geometry is so simple
that you don't need a complex mesh generator (like
[pygmsh](https://github.com/meshpro/pygmsh/),
[MeshPy](https://github.com/inducer/meshpy),
[mshr](https://bitbucket.org/fenics-project/mshr),
[pygalmesh](https://github.com/meshpro/pygalmesh/),
[dmsh](https://github.com/meshpro/dmsh/)),
but something simple and fast that makes use of the structure of the domain. Enter
meshzoo.

## Installation

Install meshzoo [from PyPI](https://pypi.org/project/meshzoo/) with

```
pip install meshzoo
```

on your machine and you're good to go.

## Examples

All generators return the points as a `(num_points, dim)` float64 array and the
cells as a `(num_cells, nodes_per_cell)` int64 array.

### Triangle

<img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/triangle.svg" width="25%">

```python
import meshzoo

bary, cells = meshzoo.triangle(8)

# corners = np.array(
#     [
#         [0.0, -0.5 * numpy.sqrt(3.0), +0.5 * numpy.sqrt(3.0)],
#         [1.0, -0.5, -0.5],
#     ]
# )
# points = np.dot(corners, bary).T

# Process the mesh, e.g., write it to a file using meshio
# meshio.write_points_cells("triangle.vtk", points, {"triangle": cells})
```

### Rectangle

<table width="100%">
  <tr width="100%">
  <td width="50%"><img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/rectangle.svg"/></td>
  <td width="50%"><img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/rectangle-quad.svg"/></td>
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

### Regular polygon

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/4gon.svg" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/6gon.svg" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/9gon.svg" width="70%"> |
| :---------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------: |
|                                   `meshzoo.ngon(4, 8)`                                    |                                   `meshzoo.ngon(6, 8)`                                    |                                   `meshzoo.ngon(9, 8)`                                    |

```python
import meshzoo

points, cells = meshzoo.ngon(5, 11)
```

### Disk

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/4gon_disk.svg" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/6gon_disk.svg" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/9gon_disk.svg" width="70%"> |
| :---------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |
|                                      `meshzoo.disk(4, 8)`                                       |                                      `meshzoo.disk(6, 8)`                                      |                                      `meshzoo.disk(9, 8)`                                      |

The disk meshes are inflations of regular polygons.

```python
import meshzoo

points, cells = meshzoo.disk(6, 11)

points, cells = meshzoo.disk_quad(10, cell_type="quad4")  # or "quad8", "quad9"
```

### Annulus

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/annulus.svg" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/annulus-quad.svg" width="70%"> |
| :-: | :-: |

```python
import meshzoo
import numpy as np

points, cells = meshzoo.annulus_tri(
    np.linspace(0.5, 1.0, 6),  # radii of the circles of points
    40,  # points per circle
    variant="zigzag",  # or "up", "down"
)

points, cells = meshzoo.annulus_quad(
    np.linspace(0.5, 1.0, 6), 40, cell_type="quad4"  # or "quad8", "quad9"
)
```

### L-shape

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/lshape.svg" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/lshape-quad.svg" width="70%"> |
| :-: | :-: |

The domain `[-1, 1]^2` without the quadrant `(0, 1]^2`, with the re-entrant
corner at the origin.

```python
import meshzoo

points, cells = meshzoo.lshape_tri(10, variant="zigzag")  # or "up", "down", "center"
points, cells = meshzoo.lshape_quad(10, cell_type="quad4")  # or "quad8", "quad9"
```

### Möbius strip

<img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/moebius.png" width="25%">

```python
import meshzoo

points, cells = meshzoo.moebius(num_twists=1, nl=60, nw=11)
```

### Sphere (surface)

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/uv_sphere.png" width="80%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/geo-sphere.png" width="60%"> |
| :--------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------: |

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

All cells are oriented such that their normals point outwards.

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/tetra-sphere.png" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/octa-sphere.png" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/icosa-sphere.png" width="70%"> |
| :-----------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: |
|                                    `meshzoo.tetra_sphere(10)`                                     |                                    `meshzoo.octa_sphere(10)`                                     |                                    `meshzoo.icosa_sphere(10)`                                     |

### Ball (solid)

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/ball-tetra.png" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/ball-hexa.png" width="70%"> |
| :---------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |

```python
import meshzoo

points, cells = meshzoo.ball_tetra(10)
points, cells = meshzoo.ball_hexa(10)
```

### Tube

<img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/tube.png" width="25%">

```python
import meshzoo

points, cells = meshzoo.tube(length=1.0, radius=1.0, n=30)
```

### Torus

<img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/torus.png" width="25%">

```python
import meshzoo

points, cells = meshzoo.torus(
    num_points_major=60, num_points_minor=20, major_radius=1.0, minor_radius=0.3
)
```

### Cube

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/cube.png" width="70%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/cube-hexa.png" width="50%"> |
| :---------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |

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

### Extrusion

Any planar mesh can be extruded along the z-axis: triangles become wedges or
tetrahedra, quadrilaterals become hexahedra. This gives, e.g., cylinders and
pipes.

| <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/cylinder.png" width="50%"> | <img src="https://raw.githubusercontent.com/meshpro/meshzoo/main/assets/pipe.png" width="50%"> |
| :-: | :-: |

```python
import meshzoo
import numpy as np

z = np.linspace(0.0, 2.0, 11)

points, tri = meshzoo.disk(6, 10)
points, wedges = meshzoo.extrude(points, tri, z)  # cylinder
points, tets = meshzoo.extrude(points, tri, z, cell_type="tetra")

points, quads = meshzoo.annulus_quad(np.linspace(0.5, 1.0, 6), 40)
points, hexa = meshzoo.extrude(points, quads, z)  # pipe
```
