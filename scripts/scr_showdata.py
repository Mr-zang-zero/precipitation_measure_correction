# coding: utf-8
"""
"""

from os import path

import matplotlib.pyplot as plt

from precipy.io import read_csv


def compare_precip(d9, d10, var='s_raw', ax=None):
    ax = ax or plt.gca()
    d9[var].cumsum().plot(ax=ax, label='rt9.1')
    d10[var].cumsum().plot(ax=ax, label='rt10')
    ax.legend()
    ax.set_ylabel('cumulative ' + var)
    return ax


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
    prefix = '2002_2015'
    d9, d10 = load_rt9_10(prefix=prefix)
    ax = compare_precip(d9, d10)
    ax.set_title(prefix)