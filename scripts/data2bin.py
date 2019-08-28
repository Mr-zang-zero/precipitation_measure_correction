# coding: utf-8
"""
Read gauge data and save in binary format.
"""

from os import path
from glob import glob

import pandas as pd

from precipy import io


DEFAULT_DATA_DIR = path.expanduser('~/data')
DEFAULT_PLUVIO_DIR = path.join(DEFAULT_DATA_DIR, 'pluvio')
DEFAULT_PKL_FILE = path.join(DEFAULT_DATA_DIR, 'pluvio.pkl')


def read_all_raw(datadir=DEFAULT_PLUVIO_DIR):
    """Read all pluvio data."""
    files = glob(path.join(datadir, '*.dat'))
    droplist = ['ws1', 'ws2', 'ws3', 'wd1', 'wd2', 'wd3', 'rh', 'frac_s']
    dats = []
    for f in files:
        print(f)
        dats.append(io.read_csv(f).drop(droplist, axis=1))
    return pd.concat(dats).sort_index()


def read_pickle(pkl_file=DEFAULT_PKL_FILE):
    return pd.read_pickle(pkl_file)


if __name__ == '__main__':
    data = read_pickle()
    data = data[data.s_raw>0].copy()
