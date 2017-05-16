# coding: utf-8

"""
Description
-----------

distutils setup.py for ccad.  View model.py for a full description of
ccad.

Author
------

View AUTHORS.

License
-------

Distributed under the GNU LESSER GENERAL PUBLIC LICENSE Version 3.
View LICENSE for details.
"""

import os
import sys
import glob
import numpy 

#import distutils.core
#import distutils.dir_util
#import distutils.sysconfig
from setuptools import setup,find_packages

name = 'ccad'
version = '0.14'  # Change also in display.py, doc/conf.py

# Include the documentation
#prefix = 'share/doc/ccad/'  # Don't like including the share prefix.
prefix = 'doc/ccad/'  
                     
data_files = [(prefix + 'html', glob.glob('doc/html/*.html')),
              (prefix + 'html/_images', glob.glob('doc/html/_images/*')),
              (prefix + 'html/_static', glob.glob('doc/html/_static/*')),
              (prefix + 'html/_sources', glob.glob('doc/html/_sources/*'))]

# Install the module
#distutils.core.setup(name=name,
setup(name=name,
      version=version,
      url='UNKNOWN',
      #py_modules=['ccad.model', 'ccad.display','ccad.quaternions'],
      #package_dir={'ccad': 'ccad'},
      data_files=data_files,
      include_dirs = [numpy.get_include()],
      #install_requires=['OCC', 'PyQt4'],
      requires=['OCC', 'PyQt4'],
      packages=find_packages()
      )
