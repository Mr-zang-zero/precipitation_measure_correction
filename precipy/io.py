# coding: utf-8
"""
tools for reading and writing files
"""

from glob import glob
from datetime import datetime, timedelta
from os import path

import numpy as np
import pandas as pd


DEFAULT_DATA_DIR = path.expanduser('~/data')
DEFAULT_PLUVIO_DIR = path.join(DEFAULT_DATA_DIR, 'pluvio')
DEFAULT_PKL_FILE = path.join(DEFAULT_DATA_DIR, 'pluvio.pkl')


def _parse_date(datestr, hourstr):
    try:
        return datetime.strptime(datestr, '%Y%m%d') + timedelta(hours=int(hourstr))
    except ValueError:
        return 0


def _parse_wd(wd):
    """parse wind direction as uint16"""
    if wd=='':
        return np.uint16(999)
    return np.uint16(wd)


def read_csv(datafile):
    header = ('date', 'hour',
              's_sov', 'l_sov', 'tot_sov', # korjattu ja sovitettu
              's_kor', 'l_kor', 'tot_kor', # korjattu
              's_raw', 'l_raw', 'tot_raw', # raaka
              'w', 't', 'rh', 'frac_s', # wind, temperature, humidity
              'ws1', 'wd1', # 10m tuuli lähiasemilla
              'ws2', 'wd2',
              'ws3', 'wd3')
    converters = {'wd1': _parse_wd,
                  'wd2': _parse_wd,
                  'wd3': _parse_wd}
    data = pd.read_csv(datafile, names=header, comment='*',
                       delim_whitespace=True, converters=converters,
                       parse_dates={'time': ['date', 'hour']},
                       date_parser=_parse_date, index_col='time').dropna()
    data['station'] = int(path.basename(datafile)[0:4])
    data.set_index(['station'], append=True, inplace=True)
    return data.reorder_levels(['station', 'time'])


def read_all_raw(datadir=DEFAULT_PLUVIO_DIR):
    """Read all pluvio data."""
    files = glob(path.join(datadir, '*.dat'))
    droplist = ['ws1', 'ws2', 'ws3', 'wd1', 'wd2', 'wd3', 'rh', 'frac_s']
    dats = []
    for f in files:
        print(f)
        dats.append(read_csv(f).drop(droplist, axis=1))
    return pd.concat(dats).sort_index()


def read_pickle(pkl_file=DEFAULT_PKL_FILE):
    return pd.read_pickle(pkl_file)

