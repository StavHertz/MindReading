# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 16:12:29 2018

@author: sarap
"""
from __future__ import print_function

import os
import sys 
import pickle 

import numpy as np 
import pandas as pd 
import scipy.signal

import matplotlib.pyplot as plt 
import seaborn as sns 
sns.set_context('talk', font_scale=1.6, rc={'lines.markeredgewidth': 2})
sns.set_style('white')
sns.set_palette('deep')


drive_path = os.path.normpath('d:/visual_coding_neuropixels')
sys.path.append(os.path.normpath('d:/resources/swdb_2018_neuropixels'))
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter 
sys.path.append(os.path.normpath('d:/resources/mindreading_repo/mindreading/sara/'))
