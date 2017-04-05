"""
Baccus lab preprocessing script

Aligns visual stimulus and recorded spike times using the photodiode

author: Niru Maheswaranathan (nirum@stanford.edu)
date: December 2nd 2015

"""

import numpy as np
from jetpack.signals import peakdet
from jetpack.ionic import notify
from jetpack.timepiece import hrtime


def find_peaks(pd, delta):
    # find peaks
    with notify('Finding peaks (can take a minute)'):
        maxtab = peakdet(pd, delta)[0]

    return maxtab


def find_start_times(maxtab, flips_per_frame=3, sampling_rate=10e3, refresh_rate=100, threshold=0.05):
    """
    Parameters
    ----------
    num_repeats : int
        The number of monitor flips per new stimulus frame. For example, a 33Hz
        stimulus shown on a 100Hz monitor has 100/33 = 3 flips per frame.

    sampling_rate : float
        Sampling rate of the photodiode recording (10kHz in the D239 setup)

    refresh_rate : float

    threshold : float between 0 and 1
        Threshold for raising warning about monitor refresh rate not compatible with
        grouping of peaks

    """

    assert len(maxtab) % flips_per_frame == 0, \
        "The number of peaks should be a multiple of the flips per frame"

    # reshape to group the peaks for the flips for a given stimulus frame
    grouped = maxtab[:,0].reshape(-1, flips_per_frame)
    assert np.abs(np.max(np.diff(grouped, axis=1) - 100)) <= threshold * refresh_rate, \
        "Peak times for a single stimulus frame should be roughly one monitor refresh apart"

    # the start times are the times of the last flip in each group (in
    # seconds), plus an offset equal to a single monitor refresh
    start_times = grouped[:, -1] / sampling_rate + 1 / refresh_rate

    print('Found {} different stimulus sequences at the following times:'.format(len(start_times)))
    for ix, t in enumerate(start_times):
        print('Stimulus #{:2} started at t = {}'.format(ix+1, hrtime(t)))

    return start_times
