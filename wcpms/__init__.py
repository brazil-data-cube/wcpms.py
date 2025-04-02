#
#    This file is part of Python Client Library for WCPMS.
#    Copyright (C) 2024 INPE.
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

from .wcpms import WCPMS, cube_query, get_phenometrics, plot_points_region, plot_phenometrics, get_collections, get_description, gpd_read_file,get_timeseries_region,get_phenometrics_region, gdf_to_geojson, plot_advanced_phenometrics,plot_points_region