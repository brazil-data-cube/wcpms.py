import urllib
import requests
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from IPython.core.display import display, HTML
from datetime import datetime

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

    html_table = '<tr>'+'<td>Code</td>'+'<td>Name</td>'+'<td>Description</td>'+'<td>Method</td>'+'<td>Value</td>'+'<td>Time</td>'+'</tr>'
    
    for item in data_json['description']:
        html_table+='<tr>'+'<td>'+item['Code']+'</td>'+'<td>'+item['Name']+'</td>'+'<td>'+item['Description']+'</td>'+'<td>'+item['Method']+'</td>'+'<td>'+str(item['Value'])+'</td>'+'<td>'+str(item['Time'])+'</td>'+'</tr>'
    
    return display(HTML('<table style="width:60%">'+html_table+'</table>')) 
