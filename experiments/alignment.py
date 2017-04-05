"""
Baccus lab preprocessing tools

aligns spiking responses across multiple repeats

author: Niru Maheswaranathan (nirum@stanford.edu)
date: December 17th 2015

"""

import numpy as np
from pyret.spiketools import binspikes, estfr
from pyret.stimulustools import upsample_stim


def extract_spikes(f, ci, ex, offset=0.0):

    cell = fmtix('cell', ci)
    assert cell in f, cell + " not found in the hdf5 file"

    expt = fmtix('expt', ex, n=1)
    assert expt in f, expt + " not found in the hdf5 file"

    tstart = np.array(f[expt]['start_time']) - offset
    tstop = np.array(f[expt]['stop_time']) - offset

    return select(f[cell], tstart, tstop)


def extract_stimulus(f, ex, upsample_factor):

    expt = fmtix('expt', ex, n=1)
    assert expt in f, expt + " not found in the hdf5 file"

    return upsample_stim(f[expt]['stim'],
                         upsample_factor,
                         time=f[expt]['timestamps'])


def extract(f, ci, ex, upsample_factor, sigma, offset):

    stim_us, time_us = extract_stimulus(f, ex, upsample_factor)

    spk = extract_spikes(f, ci, ex, offset=offset)

    dt = np.mean(np.diff(time_us))
    rate = get_rate(spk, time_us, sigma=sigma, dt=dt)

    assert len(stim_us) == len(time_us) == len(rate), "lengths not equal"

    return stim_us, time_us, spk, rate


def collect(f, ci, whichone, *args, unique=True):

    expts = np.arange(whichone, 25, 4)

    stimuli = []
    stimtimes = []
    spikes = []
    rates = []

    for ex in expts:
        stim_us, time_us, spk, rate = extract(f, ci, ex, *args)

        if unique and len(stimtimes) > 0:
            tend = stimtimes[-1][-1] + 0.01
            time_us += tend
            spk += tend

        stimuli.append(stim_us)
        stimtimes.append(time_us)
        spikes.append(spk)
        rates.append(rate)

    return stimuli, stimtimes, spikes, rates


def select(all_spikes, tstart, tstop):
    """
    Selects a subset of spikes with the given start and stop times
    """
    return all_spikes[(all_spikes >= tstart) & (all_spikes < tstop)] - tstart


def addone(array, offset=0.01):
    return np.append(array, array[-1] + offset)


def get_rate(spikes, time, sigma=0.01, dt=0.01):
    bspk, tbins = binspikes(spikes, time=addone(time, offset=dt))
    return estfr(tbins, bspk, sigma=sigma)


def fmtix(base, ix, n=2):
    return (base + '{:0%i}' % n).format(ix+1)
