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
TF_PARAMS_GH_EXP = _read_tf_params(key='sa_gh_exp_s')


def ce_exp(u, a, b, c):
    """e.g. SPICE 2018"""
    return a*np.exp(-b*u)+c


def ce_k17a(u, t, a, b, c):
    """Kochendorfer 2017a Eq. (4)"""
    return np.exp(-a*u*(1-np.arctan(b*t)+c))


def ce_spice18(u, t=None, p_vt=TF_PARAMS_GH, p_v=TF_PARAMS_GH_EXP):
    """CE based on SPICE18 recommendation"""
    p = p_v if t is None else p_vt
    u = min(u, p.u_max)
    abc = p.loc[['a', 'b', 'c']].values
    if t is not None:
        return ce_k17a(u, t, *abc)
    return ce_exp(u, *abc)


def k_old_fun(u, t, a, b, c, d):
    """functional form of correction factor for wild, tretjakov and H&H"""
    return np.exp(a+b*u+c*t+d*t*u)


def k_old(u, t, key='wild'):
    """correction factor for wild, tretjakov and H&H"""
    p = _read_tf_params(key=key)
    u = min(u, p.u_max)
    t = max(t, p.t_min)
    abcd = p.loc[['a', 'b', 'c', 'd']].values
    return k_old_fun(u, t, *abcd)


def correct_sa_data(dat):
    data = dat.copy()
    tdata = data.loc[:,['s_raw', 'w', 't']]
    tfer = lambda row: row.s_raw/ce_spice18(row.w, row.t)
    data['spice18_sa'] = tdata.apply(tfer, axis=1)
    return data