from setuptools import setup, find_packages
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'waitt_scrapers', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='waitt-scrapers',
    version=version['__version__'],
    description=('Google Sheet data scrapers for Waitt Foundation web maps: Blue Prosperity initiatives, ROC Grants, and Expeditions.'),
    long_description=long_description,
    author='Russell Moffitt',
    author_email='Russell.Moffitt@marine-conservation.org',
    url='https://github.com/bast/somepackage',
    license='MPL-2.0',
    packages=['waitt_scrapers'],
#   no dependencies in this example
    install_requires=[
      'geojson',
      'pandas',
      'xlrd',
    ],
    extras_require={
        'dev': [],
        'docs': [],
        'testing': [],
    },
    # no scripts in this example
    # scripts=['bin/a-script'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)