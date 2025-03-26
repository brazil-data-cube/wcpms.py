..
    This file is part of Python Client Library for WCPMS.
    Copyright (C) 2025 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


============================================================
Python Client Library for Web Crop Phenology Metrics Service
============================================================


.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
        :target: https://github.com/brazil-data-cube/wcpms.py/blob/master/LICENSE
        :alt: Software License


.. image:: https://readthedocs.org/projects/wcpms/badge/?version=latest
        :target: https://wcpms.readthedocs.io/en/latest/
        :alt: Documentation Status


.. image:: https://img.shields.io/badge/lifecycle-stable-green.svg
        :target: https://www.tidyverse.org/lifecycle/#stable
        :alt: Software Life Cycle


.. image:: https://img.shields.io/github/tag/brazil-data-cube/wcpms.py.svg
        :target: https://github.com/brazil-data-cube/wcpms.py/releases
        :alt: Release


.. image:: https://img.shields.io/pypi/v/wcpms
        :target: https://pypi.org/project/wcpms/
        :alt: Python Package Index


.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord


About
=====

Called Web Crop Phenology Metrics Service (WCPMS) the software extracts phenological metrics from big EO image collections, modeled as multidimensional data cubes, produced by the BDC project of INPE. 

It allows analysts to calculate phenological metrics on cloud. The opposite of the on-premises established algorithms, so with no need to download big EO data sets on their personal computers. 

We created the wcpms.py library from scratch to facilitate phenology extraction operations. This library was developed to be interoperable with other Python libraries, thus enabling users to integrate established libraries into their own workflows for pre- or post-processing and analysis. The wcpms.py library has a group of functions, the main ones are:

- ``get_collections``: returns in list format the unique identifier of each of the data cubes available in the BDC's SpatioTemporal Asset Catalogs (STAC).

- ``get_description``: returns in dictionary format the information on each of the phenology metrics, such as code, name, description and method. 	

- ``get_phenometrics``: returns in dictionary form all the phenological metrics calculated for the given spatial location.

- ``get_phenometrics_region``: returns in list format the phenological metrics calculated for each pixel centers within the boundaries of the given region using satellite images time series.


Installation
============

See `INSTALL.rst <https://github.com/brazil-data-cube/wcpms.py/blob/master/INSTALL.rst>`_.


Documentation
=============

See https://wcpms.readthedocs.io/en/latest.


References
==========


WIP


License
=======


.. admonition::
    Copyright (C) 2025 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
