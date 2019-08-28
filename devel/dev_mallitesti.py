# coding: utf-8
"""

"""
from os import path

import matplotlib.pyplot as plt

from precipy import io, correct, graph


CMAP_DEFAULT = 'rainbow'


def trans(accum_raw, u, t=None, ce=correct.ce_spice18, **kws):
    """transfer function"""
    return accum_raw/ce(u, t=t, **kws)


if __name__ == '__main__':
    plt.close('all')
    datafile = path.expanduser('~/data/2002_2014.dat')
    data = io.read_csv(datafile)
    data = data[data.tot_raw>0].copy()
    data = correct.correct_sa_data(data)
    ax1 = data.plot.scatter('s_raw', 's_kor', c='w', cmap=CMAP_DEFAULT)
    graph.plot1(ax1)
    ax2 = data.plot.scatter('s_raw', 'spice18_sa', c='w', cmap=CMAP_DEFAULT)
    graph.plot1(ax2)
