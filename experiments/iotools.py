"""
Baccus lab preprocessing io tools

Loads experiment stimuli and spikes from hdf5 and text files

author: Niru Maheswaranathan (nirum@stanford.edu)
date: December 2nd 2015

"""

import os
import json
import h5py
import numpy as np
from scipy.stats import zscore
from jetpack.ionic import notify
from jetpack.timepiece import hrtime


def read_timestamps(filename='expt.json', path='.'):

    # load expt.json file
    expt = json.load(open(os.path.join(path, filename), 'r'))

    # load timestamps from the json object
    raw_timestamps = (np.array(ex['timestamps']).flatten() for ex in expt['stim'])
    return list(map(lambda x: x - x[0], raw_timestamps))


def read_spikes(path='.'):

    # load spike files as numpy arrays
    with notify('Reading spikes from text files'):
        spikes = [np.loadtxt(f)
                  for f in sorted(os.listdir(path))
                  if (f.startswith('c') and f.endswith('.txt'))]

    print('Read spikes for {} cells.'.format(len(spikes)))

    print('Time of the first spike for each cell:')
    print('\n'.join(map(lambda x: '\t' + hrtime(x[0]), spikes)))

    print('Time of the last spike for each cell:')
    print('\n'.join(map(lambda x: '\t' + hrtime(x[-1]), spikes)))

    return spikes


def read_channel(h5file, channel=0, zscore_channels=True):

    # read the desired channel
    pd = h5file['data'][channel]

    # zscore if desired
    if zscore_channels:
        pd = zscore(pd)

    return pd
