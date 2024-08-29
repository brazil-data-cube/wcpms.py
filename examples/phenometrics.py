#
# This file is part of Python Client Library for WCPMS.
# Copyright (C) 2024 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""This example shows how to retrieve and plot a time series with phenological metrics."""

from wcpms import *

# Defines URL of a instance of the WCPMS
wcpms_url = 'https://data.inpe.br/bdc/wcpms'

# Defines a data cube query from Brazil Data Cube (BDC) 
datacube = cube_query(
    collection="S2-16D-2",
    start_date="2021-01-01",
    end_date="2021-12-31",
    freq='16D',
    band="NDVI"
)

# Retrieving the phenological metrics
pm = get_phenometrics(
    url = wcpms_url,
    cube = datacube,
    latitude=-29.202633381242652, longitude= -55.95542907714844 
)

# Visualizing the phenological metrics
print(pm)