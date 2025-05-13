#
#    This file is part of Python Client Library for WCPMS.
#    Copyright (C) 2025 INPE.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Python Client Library for Web Crop Phenology Metrics Service"""

import os
from setuptools import find_packages, setup

DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(DIR, "VERSION"), "r") as file:
    VERSION = file.read()

with open(os.path.join(DIR, "README.rst"), "r") as file:
    LONG_DESCRIPTION = file.read()

long_description = LONG_DESCRIPTION,

docs_require = [
    'Sphinx>=2.2',
    'sphinx_rtd_theme',
    'sphinx-copybutton',
]

install_requires = [
        "urllib3==2.2.2",
        "requests==2.32.3",
        "pandas==2.2.2",
        "plotly==6.0.1",
        "scipy==1.13.1",
        "datetime==5.5",
        "geopandas==1.0.1 "
]

extras_require = {
    'docs': docs_require,
}

extras_require['all'] = [ req for exts, reqs in extras_require.items() for req in reqs ]

setup(
    name='wcpms',
    packages=find_packages(),
    include_package_data=True,
    version = VERSION,
    description='Python Client of the Web Crop Phenological Metrics Service for Earth Observation Data Cubes',
    author='Brazil Data Cube Team',
    author_email = "bdc.team@inpe.br",
    url = "https://github.com/brazil-data-cube/wcpms.py",
    extras_require=extras_require,
    install_requires=install_requires,
    long_description = LONG_DESCRIPTION,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
