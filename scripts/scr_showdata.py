# coding: utf-8
"""
"""

from os import path

import pandas as pd
import matplotlib.pyplot as plt

from precipy.io import read_csv, parse_date


def compare_precip(d9, d10, var='s_raw', ax=None):
    ax = ax or plt.gca()
    d9[var].cumsum().plot(ax=ax, label='rt9.1')
    d10[var].cumsum().plot(ax=ax, label='rt10')
    ax.set_ylabel('cumulative ' + var)
    return ax

def load_hprecip():
    filee=path.expanduser('~/data/2002.p_h201503')
    header = ('date', 'hour', 'p')
    return pd.read_csv(filee, delim_whitespace=True, comment='*',
                names=header, parse_dates={'time': ['date', 'hour']},
                date_parser=parse_date, index_col='time',
                squeeze=True)

def load_rt9_10(prefix='2002_2013'):
    #f9=path.expanduser('~/data/show/show.dbg.rt9.1')
    #f10=path.expanduser('~/data/show/show.dbg.rt10.1')
    f9=path.expanduser('~/data/show/{}_rt91.show'.format(prefix))
    f10=path.expanduser('~/data/show/{}_rt10.show'.format(prefix))
    read_kw = dict(incl_station=False)
    d10=read_csv(f10, **read_kw)
    d9=read_csv(f9, **read_kw)
    return d9, d10


if __name__ == '__main__':
    plt.close('all')
    prefix = '2002_2015'
    d9, d10 = load_rt9_10(prefix=prefix)
    pc0 = d9.tot_raw.cumsum()['2015-03-01 00:00']
    p = load_hprecip()
    pc = p.cumsum() + pc0
    ax = compare_precip(d9, d10, var='tot_raw')
    pc.plot(ax=ax, label='raw')
    ax.legend()
    ax.set_title(prefix)