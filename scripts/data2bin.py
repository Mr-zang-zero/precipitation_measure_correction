# coding: utf-8
"""
Read gauge data and save in binary format.
"""
import matplotlib.pyplot as plt

from precipy import io, graph


if __name__ == '__main__':
    plt.close('all')
    data = io.read_pickle()
    data = data[data.s_kor>0.01].copy()
    #ax1 = data.plot.scatter('s_raw', 's_kor', c='w', cmap=CMAP_DEFAULT)
    #graph.plot1(ax1)
    dat = data.sample(n=5000, weights='s_raw')
    dat['dif_kor'] = dat.s_kor-dat.s_raw
    dat['dif_spice'] = dat.spice18_sa-dat.s_raw
    cmap = 'brg'
    #ax1 = dat.plot.scatter('s_raw', 's_kor', c='w', cmap=cmap)
    #ax2 = dat.plot.scatter('s_raw', 'spice18_sa', c='w', cmap=cmap)
    kws = dict(x='s_raw', c='t', edgecolor='', cmap=cmap, alpha=0.25,
               vmin=-10, vmax=3)
    fig, axarr = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), dpi=120,
                              sharex=False, sharey=True)
    dat.plot.scatter(y='dif_kor', ax=axarr[1,0], **kws)
    dat.plot.scatter(y='dif_spice', ax=axarr[1,1], **kws)
    kws.update(dict(vmin=0, vmax=6, c='w'))
    dat.plot.scatter(y='dif_kor', ax=axarr[0,0], **kws)
    dat.plot.scatter(y='dif_spice', ax=axarr[0,1], **kws)
    #ax3 = dat.plot.hexbin(x='s_raw', y='dif_spice', xscale='log', yscale='log')
    #ax3.set_xlim(left=0.3, right=5)
    #ax3.set_ylim(bottom=0.01, top=5)
    axarr[0, 0].set_title('nykyinen')
    axarr[0, 1].set_title('SPICE suositus (single Alter)')
    for ax in axarr.flatten():
        #graph.plot1(ax)
        ax.set_xlim(left=0.0, right=4)
        ax.set_ylim(bottom=-0.02, top=1)
        #ax.set_yscale('log')
        #ax.set_xscale('log')
        ax.grid('on')
        ax.set_ylabel('korjaus, mm')
    for ax in [axarr[0,0], axarr[0,1]]:
        ax.set_xlabel('')
    for ax in [axarr[1,0], axarr[1,1]]:
        ax.set_xlabel('korjaamaton, mm')
    fig.tight_layout()
