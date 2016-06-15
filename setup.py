# -*- coding: utf-8 -*-
#
import os
from setuptools import setup
import codecs

from meshzoo import __version__, __author__, __author_email__


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
      version=__version__,
      author=__author__,
      author_email=__author_email__,
      packages=['meshzoo'],
      description='A collection of meshes for numerical computation',
      long_description=read('README.rst'),
      url='https://github.com/nschloe/meshzoo',
      download_url='https://github.com/nschloe/meshzoo/releases',
      license='License :: OSI Approved :: MIT License',
      platforms='any',
      requires=['numpy'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Mathematics'
          ]
      )
