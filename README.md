# meshzoo

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/meshzoo/master.svg)](https://circleci.com/gh/nschloe/meshzoo)
[![codecov](https://codecov.io/gh/nschloe/meshzoo/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/meshzoo)
[![PyPi Version](https://img.shields.io/pypi/v/meshzoo.svg)](https://pypi.python.org/pypi/meshzoo)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/meshzoo.svg?style=social&label=Stars)](https://github.com/nschloe/meshzoo)

There are various Python tools for creating 2D and 3D FEM/FVM meshes for complex
geometries (e.g., [MeshPy](https://github.com/inducer/meshpy),
[mshr](https://bitbucket.org/fenics-project/mshr),
[frentos](https://github.com/nschloe/frentos/)). meshzoo, on the other hand,
provides an assortment of highly structured 2D and 3D meshes.

### Examples

#### Triangle
<img src="https://nschloe.github.io/meshzoo/triangle.png" width="20%">

```python
points, cells = meshzoo.triangle(3)

# Process the mesh, e.g., write it to a file using meshio
# meshio.write('rectangle.e', points, {'triangle': cells})
```

#### Rectangle
<img src="https://nschloe.github.io/meshzoo/rectangle.png" width="20%">

```python
points, cells = meshzoo.rectangle(
        xmin=0.0, xmax=1.0,
        ymin=0.0, ymax=1.0,
        nx=11, ny=11,
        zigzag=True
        )
```

#### Hexagon
<img src="https://nschloe.github.io/meshzoo/hexagon.png" width="20%">

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
points, cells = uv_sphere(num_points_per_circle=20, num_circles=10, radius=1.0)
```

<img src="https://nschloe.github.io/meshzoo/iso_sphere.png" width="20%">
```python
points, cells = iso_sphere(3)
```

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

In addition to this, the `examples/` directory contains a couple of instructive
examples for other mesh generators.


### Installation

#### Python Package Index

meshzoo is [available from the Python Package
Index](https://pypi.python.org/pypi/meshzoo/), so simply
```
pip install meshzoo -U
```
to install/upgrade.

### Testing

To run the meshzoo unit tests, check out this repository and run
```
pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. create Git tag and upload to PyPi:
    ```
    make publish
    ```

### License

meshzoo is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
