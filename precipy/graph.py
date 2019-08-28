# coding: utf-8
"""
visualization tools
"""

def plot1(ax):
    """plot 1:1 line and set aspect to 1:1"""
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    lims = (min([xlim[0], ylim[0]]), max([xlim[1], ylim[1]]))
    ax.plot(lims, lims, color='gray', label='1:1')
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_aspect('equal')