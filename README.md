# meshzoo

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/meshzoo/master.svg)](https://circleci.com/gh/nschloe/meshzoo)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/meshzoo.svg)](https://codecov.io/gh/nschloe/meshzoo)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi Version](https://img.shields.io/pypi/v/meshzoo.svg)](https://pypi.org/project/meshzoo)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/meshzoo.svg?logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/meshzoo)

When generating meshes for FEM/FVM computations, sometimes your geometry is so
simple that you don't need a complex mesh generator (like
[pygmsh](https://github.com/nschloe/pygmsh/),
[MeshPy](https://github.com/inducer/meshpy),
[mshr](https://bitbucket.org/fenics-project/mshr),
[pygalmesh](https://github.com/nschloe/pygalmesh/)),
[dmsh](https://github.com/nschloe/dmsh/)),
but something simple and fast
that makes use of the symmetries of the domain. Enter meshzoo.

### Examples

#### Triangle
<img src="https://nschloe.github.io/meshzoo/triangle.png" width="20%">

```python
import meshzoo
points, cells = meshzoo.triangle(8)

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
points, cells = meshzoo.uv_sphere(num_points_per_circle=20, num_circles=10, radius=1.0)
```

<img src="https://nschloe.github.io/meshzoo/iso_sphere.png" width="20%">

```python
points, cells = meshzoo.iso_sphere(3)
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

In addition to this, the
[`examples/`](https://github.com/nschloe/meshzoo/blob/master/examples/)
directory contains a couple of instructive examples for other mesh generators.


### Installation

meshzoo is [available from the Python Package
Index](https://pypi.org/project/meshzoo/), so simply
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
