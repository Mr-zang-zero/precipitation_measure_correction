# coding: utf-8
"""
gauge measurement correction
"""
from os import path

import numpy as np
import pandas as pd


TF_PARAMS_FILE = path.expanduser('~/koodi/sadekorjaus/tf_params.csv')


def ce_exp(u, a, b, c):
    """e.g. SPICE 2018"""
    return a*np.exp(-b*u)+c


def ce_k17a(u, t, a, b, c):
    """Kochendorfer 2017a Eq. (4)"""
    return np.exp(-a*u*(1-np.arctan(b*t)+c))


def _read_tf_params(params_file=TF_PARAMS_FILE, key='sa_gh'):
    return pd.read_csv(params_file, index_col='key').loc[key]


def ce_spice18(u, t=None, **kws):
    """CE based on SPICE18 recommendation"""
    p = _read_tf_params(**kws)
    u = u if (u < p.u_thresh) else p.u_thresh
    abc = p.loc[['a', 'b', 'c']].values
    if t is not None:
        return ce_k17a(u, t, *abc)
    raise NotImplementedError

