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

import os
import json
import urllib
import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from IPython.core.display import display, HTML
from datetime import datetime
from datetime import timedelta

class WCPMS:
    """Implement a client for WCPMS.

    .. note::

        For more information about coverage definition, please, refer to
        `WCPMS specification <https://github.com/brazil-data-cube/wcpms-spec>`_.
    """

    def __init__(self, url, access_token=None):
        """Create a WCPMS client attached to the given host address (an URL).

        Args:
            url (str): URL for the WCPMS server.
            access_token (str, optional): Authentication token to be used with the WCPMS server.
        """
        #: str: URL for the WCPMS server.
        self._url = url

        #: str: Authentication token to be used with the WCPMS server.
        self._access_token = access_token

def get_phenometrics(url, cube, latitude, longitude):
    """Returns in dictionary form all the phenological metrics calculated for the given spatial location, as well as the time series and timeline used.

    Args:
        url: The url of the available wcpms service running

        cube : Dictionary with information about a BDC's data cubes with collection, start_date, end_date, freq and band.

        longitude : (int/float) A longitude value according to EPSG:4326.

        latitude : (int/float) A latitude value according to EPSG:4326.

    Returns:
        Phenometrics: A phenological metrics object as a dictionary.
        TimeSeries: A time series object as a dictionary.

    
    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.

    Example:

        Retrieves a Phenometrics for S2-16D-2 data product:

        .. doctest::
            :skipif: WCPMS_EXAMPLE_URL is None

            >>> from wcpms import *
            >>> wcpms_url = WCPMS_EXAMPLE_URL
            >>> datacube = cube_query(
            ...                       collection="S2-16D-2",
            ...                       start_date="2021-01-01",
            ...                        end_date="2021-12-31",
            ...                       freq='16D',
            ...                       band="NDVI")
            >>> pm = get_phenometrics(
            ...                  url = wcpms_url,
            ...                  cube = datacube,
            ...                  latitude=-29.20, longitude= -55.95)
            ...
            >>> pm['phenometrics']
            {'aos_v': 2975.66650390625, 
             'bse_v': 6233.1669921875, 
             'eos_t': '2021-07-13T00:00:00', 
             'eos_v': 5489.0, 
             ...
             'sos_t': '2021-01-02T00:00:00', 
             'sos_v': 7649.0, '
             'vos_t': '2021-12-20T00:00:00', 
             'vos_v': 4817.33349609375
            }
    """
    query = dict(
        collection=cube['collection'],
        band=cube['band'],
        start_date=cube['start_date'],
        end_date=cube['end_date'],
        freq=cube['freq'],
        latitude=latitude,
        longitude=longitude,
    )

    url_suffix = '/phenometrics?'+urllib.parse.urlencode(query)

    data = requests.get(url + url_suffix) 
    data_json = data.json()

    return data_json['result']
    
def cube_query(collection, start_date, end_date, freq, band):
    """An object that contains the information associated with a collection that can be downloaded or acessed.

    Args:
        collection: String containing the collection id identifier.

        start_date : String containing the begin of a time interval. Following YYYY-MM-DD structure.
        
        end_date : String containing the begin of a time interval. Following YYYY-MM-DD structure.

        freq : String containing the frequency of images of the associated collection. Following (N-days) structure. 

        band : String containing the attribute (band) name.

    Returns:
    dictionary: A dictionary with information about a BDC's data cubes with collection, start_date, end_date, freq and band.

    
    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.
    """
    return dict(
        collection = collection,
        band = band,
        start_date = start_date,
        end_date = end_date,
        freq=freq
    )

def smooth_timeseries(ts, method='savitsky', window_length=3, polyorder=1):
    if (method=='savitsky'):
        smooth_ts = savgol_filter(x=ts, window_length=window_length, polyorder=polyorder)
    return smooth_ts

def plot_phenometrics(cube, ds_phenos):
    dates_datetime64 = pd.date_range(pd.to_datetime(cube['start_date'], format='%Y-%m-%d'), periods=len(ds_phenos['timeseries']["timeline"]), freq="16D")

    y_new = smooth_timeseries(ts=ds_phenos['timeseries']['values'], method='savitsky', window_length=2)

    plt.plot(dates_datetime64, ds_phenos['timeseries']['values'], color='blue', label='Raw NDVI') 
    plt.plot(dates_datetime64, y_new, color='red', label='Smooth NDVI') 

    p = ds_phenos["phenometrics"]

    sos_time = datetime.strptime(p['sos_t'], '%Y-%m-%dT00:00:00')
    plt.plot(sos_time, p['sos_v'], 'go', label='_nolegend_')
    plt.annotate('SOS', [sos_time, p['sos_v']])

    eos_time = datetime.strptime(p['eos_t'], '%Y-%m-%dT00:00:00')
    plt.plot(eos_time, p['eos_v'], 'go', label='_nolegend_')
    plt.annotate('EOS', [eos_time, p['eos_v']])

    pos_time = datetime.strptime(p['pos_t'], '%Y-%m-%dT00:00:00')
    plt.plot(pos_time, p['pos_v'], 'go', label='_nolegend_')
    plt.annotate('POS', [pos_time, p['pos_v']])

    vos_time = datetime.strptime(p['vos_t'], '%Y-%m-%dT00:00:00')
    plt.plot(vos_time, p['vos_v'], 'go', label='_nolegend_')
    plt.annotate('VOS', [vos_time, p['vos_v']])

    plt.axvspan(sos_time, eos_time, color='#9af8ff')

    plt.ylabel('Vegetation Health (NDVI)')
    plt.xlabel('Date')
    plt.legend(loc="upper left")

def get_collections(url):
    """List available data cubes in the BDC's SpatioTemporal Asset Catalogs (STAC).

    Args:
        url : The url of the available wcpms service running

    Returns:
    list: A list form the unique identifier of each of the data cubes available in the BDC's SpatioTemporal Asset Catalogs (STAC).


    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.

    Example:

        Retrieves available data cubes in the BDC.

        .. doctest::
            :skipif: WCPMS_EXAMPLE_URL is None

            >>> from wcpms import *
            >>> wcpms_url = WCPMS_EXAMPLE_URL
            >>> collections = get_collections(wcpms_url)
            ...
            >>> collections
            ['CBERS4-MUX-2M-1', 'CBERS4-WFI-16D-2', 'CBERS-WFI-8D-1', 'LANDSAT-16D-1', 'mod13q1-6.1', 'myd13q1-6.1', 'S2-16D-2']
    """
    url_suffix = '/list_collections'

    data = requests.get(url + url_suffix) 
    data_json = data.json()

    return data_json['coverages']

def get_description(url):
    """List the information on each of the phenological metrics, such as code, name, description and method.

    Args:
        url : The url of the available wcpms service running

    Returns:
    list: A list form the unique identifier of each of the phenological metrics, with its code, name, description and method.


    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.
    """
    url_suffix = '/describe'

    data = requests.get(url + url_suffix) 
    data_json = data.json()

    html_table = '<tr>'+'<td><b>Code</b></td>'+'<td><b>Name</b></td>'+'<td><b>Description</b></td>'+'<td><b>Method</b></td>'+'<td><b>Value</b></td>'+'<td><b>Time</b></td>'+'</tr>'
    
    for item in data_json['description']:
        html_table+='<tr>'+'<td>'+item['Code']+'</td>'+'<td>'+item['Name']+'</td>'+'<td>'+item['Description']+'</td>'+'<td>'+item['Method']+'</td>'+'<td>'+str(item['Value'])+'</td>'+'<td>'+str(item['Time'])+'</td>'+'</tr>'
    
    return display(HTML('<table style="width:90%;margin-left:5%;margin-right:5%;margin-top:5%;">'+html_table+'</table>')) 

def gpd_read_file(shapefile_dir):
    data = gpd.read_file(os.path.join(shapefile_dir))
    return data

def gdf_to_geojson(df):
    return json.loads(df.to_json())["features"][0]['geometry']

def plot_advanced_phenometrics(cube, ds_phenos, shape, start_sowing=None, end_sowing=None, start_harvesting=None, end_harvesting=None):

    ts = [] 
    tl = []
    if (ds_phenos['timeseries']):
        ts = ds_phenos['timeseries']   
        tl = ds_phenos['timeline']   
    else:
        ts = ds_phenos['timeseries']['values'] 
        tl = ds_phenos['timeseries']["timeline"]

    dates_datetime64 = pd.date_range(pd.to_datetime(cube['start_date'], format='%Y-%m-%d'), periods=len(tl), freq="16D")

    y_new = smooth_timeseries(ts=ts, method='savitsky', window_length=2)

    plt.plot(dates_datetime64, ts, color='blue', label='Raw NDVI') 
    plt.plot(dates_datetime64, y_new, color='red', label='Smooth NDVI') 

    p = ds_phenos["phenometrics"]

    sos_time = datetime.strptime(p['sos_t'], '%Y-%m-%dT00:00:00')
    plt.plot(sos_time, p['sos_v'], 'go', label='_nolegend_')
    plt.annotate('SOS', [sos_time, p['sos_v']])

    eos_time = datetime.strptime(p['eos_t'], '%Y-%m-%dT00:00:00')
    plt.plot(eos_time, p['eos_v'], 'go', label='_nolegend_')
    plt.annotate('EOS', [eos_time, p['eos_v']])

    pos_time = datetime.strptime(p['pos_t'], '%Y-%m-%dT00:00:00')
    plt.plot(pos_time, p['pos_v'], 'go', label='_nolegend_')
    plt.annotate('POS', [pos_time, p['pos_v']])

    vos_time = datetime.strptime(p['vos_t'], '%Y-%m-%dT00:00:00')
    plt.plot(vos_time, p['vos_v'], 'go', label='_nolegend_')
    plt.annotate('VOS', [vos_time, p['vos_v']])

    plt.axvspan(sos_time-timedelta(days=16), sos_time+timedelta(days=16), alpha=0.5, color='#4CBCCB')
    plt.axvspan(eos_time-timedelta(days=16), eos_time+timedelta(days=16), alpha=0.5, color='#4CBCCB', label="Uncertainty")

    if (start_sowing and end_sowing):
        v_start_sowing = shape.loc[0, start_sowing]
        v_end_sowing = shape.loc[0, end_sowing]
        plt.axvspan(v_start_sowing, v_end_sowing, color='#099c00', alpha=0.4, label=start_sowing.replace("_inicio", ""))
    
    if (start_harvesting and end_harvesting):
        v_start_harvesting = shape.loc[0, start_harvesting]  
        v_end_harvesting = shape.loc[0, end_harvesting]
        plt.axvspan(v_start_harvesting, v_end_harvesting, color='#e3c913', alpha=0.4, label=end_harvesting.replace("_fim", ""))

    plt.ylabel('Vegetation Health (NDVI)')
    plt.xlabel('Date')

    plt.legend(loc='center right', bbox_to_anchor=(1.35, 0.5))

def plot_points_region(polygon, phenos):
    x, y = [],[]
    for p in phenos:
        x.append(p["point"][0])
        y.append(p["point"][1])
    gpd.GeoSeries(polygon["geometry"]).plot(color='red', alpha=0.25)
    plt.scatter(x,y) 
    plt.show() 

def get_phenometrics_region(url, cube, geom, method, distance=None, plot_size=None):
    """List phenological metrics calculated for each of the given spatial location based on selected region methodology (all, systematic or random grid).

    Args:
        url: The url of the available wcpms service running.

        cube : Dictionary with information about a BDC's data cubes with collection, start_date, end_date, freq and band.

        geom : GeoJSON containing the geometry used to retrive phenological metrics, according to EPSG:4326.
        
        method : String containing the region methodology of images of the associated collection. The (1) all the pixels; (2) systematic grid, a N meter neighborhood distance rule; (3) random grid, N points distributed at random.

        distance (optional) : Float containing the N (number) meter neighborhood distance rule. Used on the 'systematic' method.
        
        plot_size (optional) : Int containing the N (number) of plots to be distributed at random. Used on the 'random' method.
 
    Returns:
    list: A list of dictionaries with phenological metrics calculated for each of the given spatial location.

    
    Raises:
        ConnectionError: If the server is not reachable.
        HTTPError: If the server response indicates an error.
        ValueError: If the response body is not a json document.
    """
    body = dict(
        collection=cube['collection'],
        band=cube['band'],
        start_date=cube['start_date'],
        end_date=cube['end_date'],
        freq=cube['freq'],
        geom=geom,
        method = dict(
            grid_type = method,
            plot_size = plot_size,
            distance = distance
        )
    )

    url_suffix = '/phenometrics'

    data = requests.post(url + url_suffix, json = body) 
    data_json = data.json()

    return data_json['result']