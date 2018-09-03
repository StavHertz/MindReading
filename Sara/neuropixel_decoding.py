# -*- coding: utf-8 -*-
"""
Decoding functions for running speed

Created on Fri Aug 31 00:42:40 2018

@author: sarap
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from neuropixel_running import get_running_speed, get_running_speed_by_frame

def get_frames_name(stim_type):
	"""
	From Stav's function (31Aug2018)
	"""
	if stim_type == 'natural_scenes':
		return 'frame'
	if stim_type == 'flash_250ms':
		return 'color'
	if stim_type == 'drifting_gratings' or stim_type == 'static_gratings':
		# 0.   45.   90.  135.  180.  225.  270.  315.
		return 'orientation'


def create_test_train_running_data(dataset, stim_type, c_region, frame, running, running_timestamps, running_speed):
    pre_stimulus_time = 0.05
    stimulus_length = 0.15
    natural_scenes = dataset.stim_tables[stim_type]
    # Get the presentations of one natural scenes image
    scene1 = natural_scenes[natural_scenes[get_frames_name(stim_type)] == frame]
    scene1 = get_running_speed_by_frame(running_timestamps, running_speed, scene1)
    scene1 = scene1[scene1['running'] == running]    

    # Get all the units in the region of interest
    region_units = dataset.unit_df[(dataset.unit_df['structure'] == c_region)]
    # Get the number of probes in the region
    num_of_probes = np.unique(region_units.probe.values).shape[0]
    
    num_of_trials = len(scene1)
    num_of_units = len(region_units)
    
    X = np.zeros((num_of_trials, num_of_units))
    row_i = 0
    for ind, stim_row in scene1.iterrows():
        col_i = 0
        for unit_r, unit in region_units.iterrows():
            c_probe = unit['probe']
            c_spikes = dataset.spike_times[c_probe]
            unit_spikes = c_spikes[unit['unit_id']]
            stimulus_train = unit_spikes[(unit_spikes > stim_row['start'] + pre_stimulus_time) & (unit_spikes < stim_row['start'] + pre_stimulus_time + stimulus_length)]
            X[row_i, col_i] = len(stimulus_train)
            col_i += 1
        row_i += 1
    return X, num_of_probes
