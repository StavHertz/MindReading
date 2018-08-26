# -*- coding: utf-8 -*-
"""
Demo code for gabor receptive field mapping of neuropixel data

Goals:
    - Define whether a neuron is responsive or not, strength of response
    - Compare gabor orientations at each x, y location

Created on Fri Aug 24 20:40:28 2018

@author: sarap
"""

#%% Imports
from __future__ import print_function

import os
import sys

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('talk', font_scale=2, rc={'lines.markeredgewidth': 2})
sns.set_style('white')
sns.set_palette('deep');

# %% Path-specific

drive_path = os.path.normpath('d:/visual_coding_neuropixels')
sys.path.append(os.path.normpath('d:/resources/swdb_2018_neuropixels/'))
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter
sys.path.append(os.path.normpath('d:/resources/mindreading_repo/mindreading/sara/'))
from neuropixel_plots import probe_heatmap, plot_psth, get_avg_psth

#%% Experiment specific
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')
expt_info_df = pd.read_csv(manifest_file)

# Import a 6 neuropixel probe experiment
multi_probe_filename = 'ephys_multi_58.nwb'
nwb_file = os.path.join(drive_path, multi_probe_filename)
print('Importing data file from {}'.format(nwb_file))

# Import the data file
data_set = NWB_adapter(nwb_file)

# %% Probe specific
probe_list = data_set.probe_list
print('Neuropixel probes: ', probe_list)
# Get probe-specific stuff
probe_name = 'probeE'
probe_spikes = data_set.spike_times[probe_name]
# Get all neurons recorded
unit_list = probe_spikes.keys()

#%% Stimulus specific
gabors = data_set.get_stimulus_table('gabor_20_deg_250ms')
# %% Explore the dataset:
print('Temporal frequencies: ', gabors['temporal_frequency'].unique())
print('Spatial frequencies: ', gabors['spatial_frequency'].unique())
print('Orientations: ', gabors['orientation'].unique())
# So just 1 SF, 1 TF and 3 orientations (0, 45, 90)

# Visualize the gabor centers
fig, ax = plt.subplots()
ax.plot(gabors['pos_x'], gabors['pos_y'], 'o', alpha=0.2)
ax.set_title('Electrode Positions')
#%%
gabor_analysis = gabors.copy()
for unit in unit_list:
    unit_spikes = probe_spikes[unit]
    for j, stim_row in gabor_analysis.iterrows():
        current_train
for i, row in gabor_analysis.iterrows():
    mean_fr
    
#%%

x_list = np.unique(gabors['pos_x'])
y_list = np.unique(gabors['pos_y'])
num_locs = len(x_list) * len(y_list)
print('Tested {} XY positions'.format(num_locs))
ori_list = np.unique(gabors['orientation'])
deg0_table = gabors[gabors['orientation'] == 0]

loc1 = gabors[(gabors['pos_x']==x_list[0]) & (gabors['pos_y'] == y_list[0]) &
              (gabors['orientation'] == 0)]

# %% Get each spike responses during stimulus
pre_time = 0
stim_train = {}
stim_counts = {}
xy_table = gabors[(gabors['pos_x']==x_list[0]) & (gabors['pos_y'] == y_list[0])]
for unit in unit_list:
    unit_spikes = probe_spikes[unit]
    #stim_train[unit] = []
    stim_counts[unit] = np.zeros_like(ori_list)
    for i, ori in enumerate(ori_list):
         ori_table = xy_table[xy_table['orientation'] == ori]
         for j, stim_row in ori_table.iterrows():
             current_train = unit_spikes[(unit_spikes > stim_row['start'] - pre_time) & (unit_spikes <= stim_row['end'])] - stim_row['start']
             #stim_train[unit].append(current_train)
             stim_counts[unit][i] = stim_counts[unit][i] + len(current_train)

# %%
def spikes_around_stim(spikes, start_times, stop_times, pre_time=0, tail_time=0):
	spike_train = []
	for start, stop in zip(start_times, stop_times):
		current_train = spikes[(spikes > start-pre_time) & (spikes <= stop+tail_time)]
		current_train = current_train - start
		spike_train.append(current_train)
	return spike_train
# %%
x = spikes_around_stim(unit_spikes, loc1['start'].values, loc1['end'].values)
