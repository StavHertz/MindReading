# -*- coding: utf-8 -*-
"""
Demo code for gabor receptive field mapping of neuropixel data

A general outline to create rough RF maps.
Used to generate the .pkl files used by later Gabor analysis functions

Created on Fri Aug 24 20:40:28 2018

@author: sarap
"""

#%% Imports
from __future__ import print_function

import os
import sys
import pickle

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('talk', font_scale=2, rc={'lines.markeredgewidth': 2})
sns.set_style('white')
sns.set_palette('deep');

# %% Path-specific
drive_path = os.path.normpath('d:/visual_coding_neuropixels')
rf_path = os.path.normpath('d:/RFMaps/')
sys.path.append(os.path.normpath('d:/resources/swdb_2018_neuropixels/'))
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter
sys.path.append(os.path.normpath('d:/resources/mindreading_repo/mindreading/sara/'))
from neuropixel_plots import probe_heatmap, region_cmap
from neuropixel_spikes import get_avg_psth

#%% Experiment specific
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')
expt_info_df = pd.read_csv(manifest_file)

# Import a 6 neuropixel probe experiment
multi_probe_filename = 'ephys_multi_89.nwb'
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

x_list = np.unique(gabors['pos_x'])
y_list = np.unique(gabors['pos_y'])
num_locs = len(x_list) * len(y_list)
ori_list = np.unique(gabors['orientation'])

print('Tested {} XY positions'.format(num_locs))

# Visualize the gabor centers
fig, ax = plt.subplots()
ax.plot(gabors['pos_x'], gabors['pos_y'], 'o', alpha=0.2)
ax.set_title('Gabor Positions')


#%% Average PSTHs for each unique combination of x, y and orientation
data = []
for unit in unit_list:
    unit_spikes = probe_spikes[unit]
    region_name = probe_df[probe_df['unit_id']=='1']['structure'].values[0]
    for i, x in enumerate(x_list):
        for j, y in enumerate(y_list):
            for k, t in enumerate(ori_list):
                tmp_df = gabors[(gabors['pos_x']==x) & (gabors['pos_y']==y) & (gabors['orientation']==t)]
                psth, centers = get_avg_psth(tmp_df, unit_spikes)
                resp = np.sum(psth[centers > 0])
                ind = str(i) + str(j) + str(k)
                data.append([ind, unit, region_name, x, y, t, psth, resp])
gabor_analysis = pd.DataFrame(data, columns=['stim_id', 'unit_id', 'structure', 'x', 'y', 't', 'psth', 'resp'])
print('Total stimulus combinations: ', len(x_list)*len(y_list)*len(ori_list))

#%% Save
path_name = os.path.normpath(rf_path + '\\' + probe_name + '_gabor_rf.pkl')
f = open(os.path.normpath(rf_path + '\\' + probe_name + '_gabor_rf.pkl'), 'wb')
pickle.dump(gabor_analysis, f)
f.close()

#%% Map the receptive fields of all units
for unit in unit_list:
    rf_map = np.finfo(float).eps + np.zeros(shape=[3, len(x_list), len(y_list)])
    unit_analysis = gabor_analysis[gabor_analysis['unit_id'] == unit]
    for i, x in enumerate(x_list):
        for j, y in enumerate(y_list):
            for k, t in enumerate(ori_list):
                ind = np.where(unit_analysis['stim_id'] == str(i)+str(j)+str(k))
                rf_map[k, i, j] = unit_analysis['resp'].values[ind]
    # Only plot the units that actually spiked
    if rf_map.max() == 0:
        continue
    # Normalize the receptive field map by the maximum value
    norm_map = rf_map/rf_map.max()
    # Make a single map from preferred orientations
    norm_map = np.max(norm_map, axis=0)
    fig, ax = plt.subplots(1, 1, figsize=(4,4))
    sns.heatmap(norm_map, square=True, cbar=False, xticklabels=False, yticklabels=False, cmap=region_cmap(unit_analysis['structure'].values[0]))
    ax.set_title('Unit {}, {}, {}'.format(unit, unit_analysis['structure'].values[0], probe_name))   
    fig.savefig(os.path.normpath('{}\\{}_{}_gabor_rf.png'.format(rf_path, probe_name, unit)))
