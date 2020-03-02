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
    ax.set_title(var)


def load_rt9_10():
    f9=path.expanduser('~/data/show/show.dbg.rt9.1')
    f10=path.expanduser('~/data/show/show.dbg.rt10.1')
    d10=read_csv(f10)
    d9=read_csv(f9)
    return d9, d10


