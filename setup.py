# -*- coding: utf-8 -*-
#
import os
from setuptools import setup
import codecs

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, 'meshzoo', '__about__.py')) as f:
    exec(f.read(), about)


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except Exception:
        content = ''
    return content


setup(name='meshzoo',
      version=about['__version__'],
      author=about['__author__'],
      author_email=about['__author_email__'],
      packages=['meshzoo'],
      description='A collection of meshes for numerical computation',
      long_description=read('README.rst'),
      url='https://github.com/nschloe/meshzoo',
      download_url='https://github.com/nschloe/meshzoo/releases',
      license=about['__license__'],
      platforms='any',
      install_requires=[
          'numpy'
          ],
      classifiers=[
          about['__status__'],
          about['__license__'],
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Mathematics'
          ]
      )
