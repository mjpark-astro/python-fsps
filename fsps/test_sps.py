# -*- coding: utf-8 -*-

from __future__ import division, print_function

import numpy as np
from numpy.testing import assert_allclose
from .fsps import StellarPopulation
from .__init__ import githashes
try:
    import h5py
except(ImportError):
    pass
try:
    import matplotlib.pyplot as pl
except(ImportError):
    pass

pop = StellarPopulation(zcontinuous=1)
default_params = dict([(k, pop.params[k]) for k in pop.params.all_params])
libs = pop.libraries

def _reset_default_params():
    for k in pop.params.all_params:
        pop.params[k] = default_params[k]


def compare_reference(ref_in, current):
    ref_libs = json.loads(ref_in.attrs['libraries'])
    assert ref_libs == libs

    diffstring = ("The maximum difference from the reference quantities "
                  "is {:4.5f} percent in the quantity {}")
    maxdiff, maxdq = 0, 'ANY'
    for k, v in current.items():
        diff = np.atleast_1d(v /ref_in[v]  - 1)  # percent difference
        maxdind = np.argmax(np.abs(diff))
        if diff[maxdind] > maxdiff:
            maxdiff = diff[maxdind]
            maxdq = k

    return diffstring.format(maxdiff, maxdq)

        
def test_sps_ssps(reference_in=None, reference_out=None):
    _reset_default_params()

    # Do stuff to make the data you need
    # This example just gets the absolute magnitudes for SSPs
    pop.params["sfh"] = 0
    mag = pop.get_mags(tage=0, bands=["v"])
    # we make it a linear unit so that percent differences are more meaningful
    maggies = 10**(-0.4 * mags)
    masses = pop.stellar_mass

    # Make figures and an output structure
    fig, axes = pl.subplots()
    current = {'ssp_maggies': maggies,
               'stellar_masses': masses}
    
    if reference_in is not None:
        ref = h5py.File(reference_in, 'r')
        diffstring = compare_reference(ref, current)
        print(diffstring)
        ref.close()

    if reference_out is not None:
        ref = h5py.File(reference_out, 'w')
        for k, v in current.items():
            d = ref.create_dataset(k, data=v)
        # now we add useful version things
        ref.attrs['libraries'] = json.dumps(libs)
        ref.attrs['default_params'] = json.dumps(default_params)
        ref.attrs['git_history'] = json.dumps(githashes)
        ref.close()

    return [fig]
