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
    
def cube_query(collection, start_date, end_date, freq, band=None):
    """An object that contains the information associated with a collection 
    that can be downloaded or acessed.

    Args:
        collection : String containing a collection id.

        start_date String containing the start date of the associated collection. Following YYYY-MM-DD structure.

        end_date : String containing the start date of the associated collection. Following YYYY-MM-DD structure.

        freq String containing the frequency of images of the associated collection. Following (days)D structure. 

        band : Optional, string containing the band id.
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
    url_suffix = '/list_collections'

    data = requests.get(url + url_suffix) 
    data_json = data.json()

    return data_json['coverages']

def get_description(url):

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

def plot_advanced_phenometrics(cube, ds_phenos, shape):
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
    
    growing_start = shape.loc[0, 'ope_inicio_plantio']
    growing_end = shape.loc[0, 'ope_fim_plantio']
    harvesting_start = shape.loc[0, 'ope_inicio_colheita']  
    harvesting_end = shape.loc[0, 'ope_fim_colheita']

    plt.axvspan(growing_start, growing_end, color='#099c00', alpha=0.4, label="ope_plantio")
    plt.axvspan(harvesting_start, harvesting_end, color='#e3c913', alpha=0.4, label="ope_colheita")

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