# coding: utf-8
"""
gauge measurement correction
"""
from os import path

import numpy as np
import pandas as pd


TF_PARAMS_FILE = path.join(path.dirname(__file__), 'tf_params.csv')


def _read_tf_params(params_file=TF_PARAMS_FILE, key='sa_gh'):
    """Read transfer function parameters."""
    return pd.read_csv(params_file, index_col='key').loc[key]


TF_PARAMS_GH = _read_tf_params()


def ce_exp(u, a, b, c):
    """e.g. SPICE 2018"""
    return a*np.exp(-b*u)+c


def ce_k17a(u, t, a, b, c):
    """Kochendorfer 2017a Eq. (4)"""
    return np.exp(-a*u*(1-np.arctan(b*t)+c))


def ce_spice18(u, t=None, p=TF_PARAMS_GH):
    """CE based on SPICE18 recommendation"""
    u = u if (u < p.u_thresh) else p.u_thresh
    abc = p.loc[['a', 'b', 'c']].values
    if t is not None:
        return ce_k17a(u, t, *abc)
    raise NotImplementedError


def correct_sa_data(dat):
    data = dat.copy()
    tdata = data.loc[:,['s_raw', 'w', 't']]
    tfer = lambda row: row.s_raw/ce_spice18(row.w, row.t)
    data['spice18_sa'] = tdata.apply(tfer, axis=1)
    return data