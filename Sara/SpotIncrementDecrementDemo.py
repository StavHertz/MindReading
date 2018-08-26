# -*- coding: utf-8 -*-
"""
Spot stimulus analysis demo

Created on Sat Aug 25 13:22:44 2018

@author: sarap
"""

from __future__ import print_function

import os
import sys

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('notebook', font_scale=1.5, rc={'lines.markeredgewidth': 2})
sns.set_style('white')
sns.set_palette('deep');

# %% Settings
pre_time = 0.1
bin_width = 0.005
probe_spacing = 20  # Microns
bins = [x*bin_width for x in range(-20,51)]

# %% Generic
drive_path = os.path.normpath('d:/visual_coding_neuropixels')
image_path = os.path.normpath('d:/Images/stimuli/')
sys.path.append(os.path.normpath('d:/resources/swdb_2018_neuropixels/'))
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter
sys.path.append(os.path.normpath('d:/resources/mindreading_repo/mindreading/sara/'))
from neuropixel_plots import probe_heatmap

manifest_file = os.path.join(drive_path,'ephys_manifest.csv')

# Create experiment dataframe
expt_info_df = pd.read_csv(manifest_file)
#make new dataframe by selecting only multi-probe experiments
multi_probe_expt_info = expt_info_df[expt_info_df.experiment_type == 'multi_probe']
multi_probe_example = 3 # index to row in multi_probe_expt_info
multi_probe_filename  = multi_probe_expt_info.iloc[multi_probe_example]['nwb_filename']

nwb_file = os.path.join(drive_path, multi_probe_filename)
print('Importing data file from {}'.format(nwb_file))


data_set = NWB_adapter(nwb_file)
probe_list = data_set.probe_list
print('Neuropixel probes: ', probe_list)

# %% Probe
probe_name = 'probeE'
probe_spikes = data_set.spike_times[probe_name]
# Get all neurons recorded
unit_list = probe_spikes.keys()
print('Identified {} units'.format(len(unit_list)))
# Subset of dataframe corresponding to chosen probe
probe_df = data_set.unit_df[(data_set.unit_df['probe']==probe_name)]

# %% Correct unit lists
# Not sure why this is necessary
unit_list = np.intersect1d(unit_list, probe_df['unit_id'])
probe_df = probe_df[probe_df['unit_id'].isin(unit_list)]

probe_spacing = 20  # microns

# %% Grating stimulus
sg_table = data_set.get_stimulus_table('static_gratings')

# Stimulus information
print('Spatial frequencies: ', sg_table['spatial_frequency'].unique())
print('Orientations: ', sg_table['orientation'].unique())
print('Phases: ', sg_table['phase'].unique())

# %% Spot stimulus
spot_table = data_set.get_stimulus_table('flash_250ms')
inc_table = spot_table[spot_table['color'] == 1]
dec_table = spot_table[spot_table['color'] == -1]


# %% PSTH
pre_time = 0.1
dec_counts = []  # List to hold the PSTHs of each electrode
for unit in unit_list:
    spike_train = probe_spikes[unit]
    stim_train = []
    for j, stim_row in dec_table.iterrows():
        current_train = spike_train[(spike_train > stim_row['start'] - pre_time) & (spike_train <= stim_row['end'])] - stim_row['start']
        stim_train.append(current_train)
    counts, edges = np.histogram(np.hstack(stim_train), bins=bins)
    dec_counts.append(counts)

inc_counts = []
for unit in unit_list:
    spike_train = probe_spikes[unit]
    stim_train = []
    for j, stim_row in inc_table.iterrows():
        current_train = spike_train[(spike_train > stim_row['start'] - pre_time) & (spike_train <= stim_row['end'])] - stim_row['start']
        stim_train.append(current_train)
    counts, edges = np.histogram(np.hstack(stim_train), bins=bins)
    inc_counts.append(counts)
# Centers of each time bin
centers = edges[:-1] - np.diff(edges)/2

# %% Analyze the decrements
dec_analysis_df = probe_df.copy()
dec_analysis_df['counts'] = dec_counts

# Get a list of unique depths
dec_depth_list = dec_analysis_df['depth'].unique()
dec_xdepth = np.arange(np.min(dec_depth_list), 0, probe_spacing)

# Create the count matrix
dec_count_matrix = np.zeros([len(dec_xdepth), len(dec_counts[0])])

for i, row in dec_analysis_df.iterrows():
    dec_count_matrix[np.where(dec_xdepth == row['depth'])] = row['counts']

# %% Now the increments
inc_analysis_df = probe_df.copy()
inc_analysis_df['counts'] = inc_counts
inc_count_matrix = np.zeros_like(dec_count_matrix)


# Get a list of unique depths
inc_depth_list = inc_analysis_df['depth'].unique()
inc_xdepth = np.arange(np.min(inc_depth_list), 0, probe_spacing)

# Create the count matrix
inc_count_matrix = np.zeros([len(inc_xdepth), len(inc_counts[0])])

for i, row in inc_analysis_df.iterrows():
    inc_count_matrix[np.where(inc_xdepth == row['depth'])] = row['counts']

# %% Plot the heatmaps
dec_fig, ax = probe_heatmap(dec_count_matrix, dec_xdepth, edges, pre_time=pre_time)
ax.set_title('Probe{} - Spot decrements'.format(probe_name[-1]), fontsize=25)
ax.set_xticklabels([])

inc_fig, ax = probe_heatmap(inc_count_matrix, inc_xdepth, edges, pre_time=pre_time)
ax.set_title('Probe{} - Spot increments'.format(probe_name[-1]))
ax.set_xticklabels([])
# %% Save the figures
inc_fig.savefig(os.path.normpath(image_path + '/' + probe_name + '_' + 'spot_inc' + '_heatmap.png'))
dec_fig.savefig(os.path.normpath(image_path + '/' + probe_name + '_' + 'spot_dec' + '_heatmap.png'))
