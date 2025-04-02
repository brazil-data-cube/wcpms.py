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


Changes
=======

Version 0.2.0 (2025-04-02)
--------------------------
- Added get_collections Example - Included a practical usage example for the get_collections function.
- Reworked Plot Function Using Plotly - Updated the plotting function to Plotly, instead of matplotlib, for interactive and dynamic visualizations.
- Reworked get_phenometrics_region Function - List phenological metrics calculated for each spatial location within the boundaries of the given region.
- Added get_timeseries_region Function - New function to retrieves the satellite images time series for each pixel centers within the boundaries of the given region.
- Remade Jupyter Notebooks - Updated and restructured Jupyter notebooks to reflect new functionalities, and add step-by-step guidance for users.
- Updated Documentation - Revised and expanded documentation to include new features and improve readability.

Version 0.1.0 (2025-03-10)
--------------------------

- Add get_phenometrics - Returns in dictionary form all the phenological metrics calculated for the given spatial location.
- Add cube_query - An object that contains the information associated with a collection that can be downloaded or acessed.
- Add get_collections - List available data cubes in the BDC's SpatioTemporal Asset Catalogs (STAC).
- Add get_description - List the information on each of the phenological metrics, such as code, name, description and method.
- Add get_phenometrics_region - List phenological metrics calculated for each of the given spatial location based on selected region methodology (all, systematic or random grid).

