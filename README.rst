..
    This file is part of Python Client Library for WCPMS.
    Copyright (C) 2024 INPE.

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


=================================================
Python Client Library for Web Crop Phenology Metrics Service
=================================================


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

The Web Crop Phenology Metrics Service (WCPMS) is an web service for calculating phenological metrics based on Phenolopy library and EO Data from the Brazil Data Cube (BDC). It will allow analysts to calculate phenological metrics from data cubes without downloading big EO datasets to their personal computers.

The software run on the server side, so it doesn't require package installation. Through a simple API, analysts indicate a spatial location or region and the WCPMS will retrieve the phenological metrics associated with spatial locations by calculating it using time series. 

The WCPMS is a web service, and it can be accessed through its API. To facilitate these operations, we have developed an official client—a simple Python library. The WCPMS Client is composed of a group of functions, the main ones are:

- ``get_collections``: returns in list format the unique identifier of each of the data cubes available in the BDC’s SpatioTemporal Asset Catalogs (STAC).

- ``get_description``: returns in dictionary format the information on each of the phenology metrics, such as code, name, description and method. 	

- ``get_phenometrics``: returns in dictionary form all the phenological metrics calculated for the given spatial location.

- ``get_phenometrics_region``: returns in list form dictionary with the phenological metrics calculated for each of the given spatial location based on selected region methodology (all, systematic grid or random grid).



Installation
============

See `INSTALL.rst <./INSTALL.rst>`_.


Using WCPMS in the Command Line
==============================

See `CLI.rst <./CLI.rst>`_.


Documentation
=============


WIP


References
==========


WIP


License
=======


.. admonition::
    Copyright (C) 2024 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
