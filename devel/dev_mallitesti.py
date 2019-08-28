# coding: utf-8
"""

"""
from os import path

import matplotlib.pyplot as plt

import pysade.io
import pysade.correct


CMAP_DEFAULT = 'rainbow'


def trans(accum_raw, u, t=None, ce=pysade.correct.ce_spice18, **kws):
    """transfer function"""
    return accum_raw/ce(u, t=t, **kws)


def plot1(ax):
    """plot 1:1 line"""
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    lims = (min([xlim[0], ylim[0]]), max([xlim[1], ylim[1]]))
    ax.plot(lims, lims, color='gray', label='1:1')
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_aspect('equal')


if __name__ == '__main__':
    plt.close('all')
    datafile = path.expanduser('~/data/2002_2014.dat')
    data = pysade.io.read_csv(datafile)
    data = data[data.tot_raw>0].copy()
    ax1 = data.plot.scatter('s_raw', 's_kor', c='w', cmap=CMAP_DEFAULT)
    plot1(ax1)
    tdata = data.loc[:,['s_raw', 'w', 't']]
    tfer = lambda row: row.s_raw/pysade.correct.ce_spice18(row.w, row.t, key='sa_gh')
    data['spice18_sa'] = tdata.apply(tfer, axis=1)
    ax2 = data.plot.scatter('s_raw', 'spice18_sa', c='w', cmap=CMAP_DEFAULT)
    plot1(ax2)
