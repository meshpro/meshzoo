# Mesh Zoo

[![Build Status](https://travis-ci.org/nschloe/meshzoo.svg?branch=master)](https://travis-ci.org/nschloe/meshzoo)
[![codecov](https://codecov.io/gh/nschloe/meshzoo/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/meshzoo)


There are various Python tools assisting with mesh generation for numerical
computation. This repostory contains some instructive examples for

  * [MeshPy](https://github.com/inducer/meshpy),
  * [pygmsh](https://github.com/nschloe/pygmsh),
  * [mshr](https://bitbucket.org/fenics-project/mshr),

and a few simple custom meshes.

### Examples

![](https://nschloe.github.io/meshzoo/hexagon.png)
![](https://nschloe.github.io/meshzoo/pacman.png)
![](https://nschloe.github.io/meshzoo/moebius.png)
![](https://nschloe.github.io/meshzoo/tetrahedron.png)
![](https://nschloe.github.io/meshzoo/screw.png)
![](https://nschloe.github.io/meshzoo/toy.png)

### Testing

To run the Mesh Zoo unit tests, check out this repository and run
```
nosetests
```
or
```
nose2 -s test
```

### License

Mesh Zoo is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
