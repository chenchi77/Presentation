
from __future__ import print_function

import sys

if sys.version_info < (2, 7):
  print('presentation requires python version >= 2.7.',
        file=sys.stderr)
  sys.exit(1)
if (3, 1) <= sys.version_info < (3, 3):
  print('presentation requires python3 version >= 3.3.',
        file=sys.stderr)
  sys.exit(1)

from setuptools import setup

packages = [
    'presentation',
]

install_requires = [
    'google-api-python-client>=1.6.4',
]

long_desc = """Create Presentation by Google Slides and Google Drive"""

import presentation
version = presentation.__version__

setup(
    name="presentation",
    version=version,
    description="Google API Client Library for Python",
    long_description=long_desc,
    author="Charlie Chen",
    url="https://github.com/chenchi77/Presentation",
    install_requires=install_requires,
    packages=packages,
    package_data={},
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)