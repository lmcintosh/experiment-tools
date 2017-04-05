from setuptools import setup, find_packages
import os
import sys
import experiments

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''

setup(name='experiments',
      version=experiments.__version__,
      author='Niru Maheswaranathan and Lane McIntosh',
      author_email='lmcintosh@stanford.edu',
      url='https://github.com/lmcintosh/experiment-tools',
      packages=find_packages(),
      py_modules=['photodiode', 'iotools', 'utils', 'alignment'],
      )
