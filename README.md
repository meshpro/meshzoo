# meshzoo

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/meshzoo/master.svg?style=flat-square)](https://circleci.com/gh/nschloe/meshzoo)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/meshzoo.svg?style=flat-square)](https://codecov.io/gh/nschloe/meshzoo)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/meshzoo.svg?style=flat-square)](https://pypi.org/pypi/meshzoo/)
[![PyPi Version](https://img.shields.io/pypi/v/meshzoo.svg?style=flat-square)](https://pypi.org/project/meshzoo)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/meshzoo.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/meshzoo)
[![PyPi downloads](https://img.shields.io/pypi/dm/meshzoo.svg?style=flat-square)](https://pypistats.org/packages/meshzoo)

When generating meshes for FEM/FVM computations, sometimes your geometry is so simple
that you don't need a complex mesh generator (like
[pygmsh](https://github.com/nschloe/pygmsh/),
[MeshPy](https://github.com/inducer/meshpy),
[mshr](https://bitbucket.org/fenics-project/mshr),
[pygalmesh](https://github.com/nschloe/pygalmesh/),
[dmsh](https://github.com/nschloe/dmsh/)),
but something simple and fast that makes use of the symmetries of the domain. Enter
meshzoo.

### Examples

#### Triangle
<img src="https://nschloe.github.io/meshzoo/triangle.svg" width="20%">

```python
import meshzoo
points, cells = meshzoo.triangle(8)

# Process the mesh, e.g., write it to a file using meshio
# meshio.write_points_cells('rectangle.vtk', points, {'triangle': cells})
```

#### Rectangle
<img src="https://nschloe.github.io/meshzoo/rectangle.svg" width="20%">

```python
points, cells = meshzoo.rectangle(
        xmin=0.0, xmax=1.0,
        ymin=0.0, ymax=1.0,
        nx=11, ny=11,
        zigzag=True
        )
```

#### Hexagon
<img src="https://nschloe.github.io/meshzoo/hexagon.svg" width="20%">

```python
points, cells = meshzoo.hexagon(3)
```

#### Möbius strip
<img src="https://nschloe.github.io/meshzoo/moebius.png" width="20%">

```python
points, cells = meshzoo.moebius(num_twists=1, nl=60, nw=11)
```

#### Sphere (surface)
<img src="https://nschloe.github.io/meshzoo/uv_sphere.png" width="20%">

```python
points, cells = meshzoo.uv_sphere(num_points_per_circle=20, num_circles=10, radius=1.0)
```

Spheres can also be generated by refining the faces of [platonic
solids](https://en.wikipedia.org/wiki/Platonic_solid) and then "inflating" them. meshzoo
implements a few of them. The sphere generated from the icosahedron has the
highest-quality (most equilateral) triangles.

| <img src="https://nschloe.github.io/meshzoo/tetra-sphere.png" width="70%"> | <img src="https://nschloe.github.io/meshzoo/octa-sphere.png" width="70%"> | <img src="https://nschloe.github.io/meshzoo/icosa-sphere.png" width="70%"> |
| :----: | :---: | :---: |
|`meshzoo.tetra_sphere(10)` | `meshzoo.octa_sphere(10)` | `meshzoo.icosa_sphere(10)` |


#### Tube
<img src="https://nschloe.github.io/meshzoo/tube.png" width="20%">

```python
points, cells = meshzoo.tube(length=1.0, radius=1.0, n=30)
```

#### Cube
<img src="https://nschloe.github.io/meshzoo/cube.png" width="20%">

```python
points, cells = meshzoo.cube(
        xmin=0.0, xmax=1.0,
        ymin=0.0, ymax=1.0,
        zmin=0.0, zmax=1.0,
        nx=11, ny=11, nz=11
        )
```


### Extra, extra

In addition to this, the
[`examples/`](https://github.com/nschloe/meshzoo/blob/master/examples/) directory
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

meshzoo is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
