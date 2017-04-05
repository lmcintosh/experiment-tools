"""
Experiment management
author: Niru Maheswaranathan
5:13 AM Jan 4, 2013
"""

import numpy as np
import re, pickle
from functools import partial
from os import listdir                               # Finding files
from os.path import join, expanduser, exists, isfile # Pathnames
from datetime import datetime                        # handling dates
from scipy.io import loadmat

def loadstim(expt, fullDir):
    """
    Loads a stimulus .mat file
    """
    stim = loadmat(join(fullDir, 'stim' + str(expt) + '.mat'))
    return stim

def loadfile(fname, fullDir):
    data = np.load(join(fullDir, fname))

    # return either the only key or the whole dictionary
    if len(data.keys()) == 1:
        return data[data.keys()[0]]
    else:
        return data
