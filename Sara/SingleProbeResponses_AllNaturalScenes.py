# -*- coding: utf-8 -*-
"""
Single probe average PSTH of all trials for all natural scenes.

Creates plots per region and for the entire probe

Created on Fri Aug 24 15:33:24 2018

@author: sarap
"""
from __future__ import print_function
import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

# Settings
probe_name = 'probeC'
pre_time = 0.1
bin_width = 0.005
bins = [x*bin_width for x in range(-20,51)]
scale_psth = 1  # multiplier to PSTHs for visibility
fig_name = 'Probe{}_AllImages'.format(probe_name[-1])

drive_path = os.path.normpath('d:/visual_coding_neuropixels')
sys.path.append(os.path.normpath('d:/resources/swdb_2018_neuropixels/'))
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')

# Create experiment dataframe
expt_info_df = pd.read_csv(manifest_file)
#make new dataframe by selecting only multi-probe experiments
multi_probe_expt_info = expt_info_df[expt_info_df.experiment_type == 'multi_probe']
multi_probe_example = 1 # index to row in multi_probe_expt_info
multi_probe_filename  = multi_probe_expt_info.iloc[multi_probe_example]['nwb_filename']

nwb_file = os.path.join(drive_path, multi_probe_filename)
print('Importing data file from {}'.format(nwb_file))
image_path = os.path.normpath('D:\\Images\\AvgOverImages\\' + multi_probe_filename[:-4])
print('Saving output to {}'.format(image_path))

data_set = NWB_adapter(nwb_file)
probe_spikes = data_set.spike_times[probe_name]

ns_table = data_set.get_stimulus_table('natural_scenes')
all_trains = {}
# Subset of dataframe corresponding to chosen probe
probe_df = data_set.unit_df[(data_set.unit_df['probe']==probe_name)]
# Sort by depth so iterrows naturally runs in depth order
probe_df.sort_values('depth', ascending=False)

for i, unit_row in probe_df.iterrows():
    spike_train = probe_spikes[unit_row['unit_id']]
    stim_train = []
    for image_id in np.unique(ns_table['frame']):
        frame_table = ns_table[ns_table.frame == image_id]
        for j, stim_row in frame_table.iterrows():
            current_train = spike_train[(spike_train > stim_row['start'] - pre_time) & (spike_train <= stim_row['end'])] - stim_row['start']
            stim_train.append(current_train)
    all_trains[unit_row['unit_id']] = stim_train  

# PSTH calculation & plotting
all_counts = []
fig,ax = plt.subplots(1,1,figsize=(15,20))
for i, unit_row in probe_df.iterrows():
    counts, edges = np.histogram(np.hstack(all_trains[unit_row['unit_id']]), bins=bins)
    plt.plot(edges[1:], unit_row['depth']+scale_psth * counts)
    all_counts.append(counts)        
ax.set_ylabel('Depth')
ax.axvspan(-0.2,0,color='gray',alpha=0.2);
ax.set_xlim([-0.1, 0.25])
ax.set_xlabel('Time (sec)')
fig.savefig(os.path.normpath('D:\\Images\\AvgOverImages\\' + fig_name + '_psth.png'))	

        
# Heat map
fig,ax = plt.subplots(1,1,figsize=(15,20))
plt.imshow(np.vstack(all_counts))
ax.set_title(fig_name)
fig.savefig(os.path.normpath('D:\\Images\\AvgOverImages\\' + fig_name + '_heatmap.png'))

# Split by brain region
all_regions = probe_df['structure'].unique()
print('Probe{} has {} structures: '.format(probe_name[-1], len(all_regions)))
print(all_regions)

# Plot to subplots
fig,ax = plt.subplots(len(all_regions), 1, figsize=(10,25))
ax.flatten()
region_counts = {}
region_depths = {}
for i, region_name in enumerate(all_regions):
    region_counts[region_name] = []
    region_depths[region_name] = []
    region_df = probe_df[probe_df['structure'] == region_name]
    for j, row in region_df.iterrows():
        counts, edges = np.histogram(np.hstack(all_trains[row['unit_id']]), bins=bins)
        ax[i].plot(edges[1:], row['depth'] + counts, linewidth=0.7)
        region_counts[region_name].append(counts)
        region_depths[region_name].append(row['depth'])
    
    ax[i].set_title('Probe{} - {} PSTH'.format(probe_name[-1], region_name))
    ax[i].set_ylabel('Depth')
    ax[i].axvspan(-0.2,0,color='gray',alpha=0.2);
    ax[i].set_xlim([-0.1, 0.25])
ax[-1].set_xlabel('Time (ms)')
fig.savefig(os.path.normpath('D:\\Images\\AvgOverImages\\' + probe_name + '_regions.png'))

# Individual plots per region (uses values calculated above)
bin_centers = 1e3 * (edges[1:] - (edges[1]-edges[0])/2)  # in ms now
for i, region_name in enumerate(all_regions):
    fig, ax = plt.subplots(1,1, figsize=(7,10))
    for j in range(len(region_counts[region_name])):
        ax.plot(1000*(edges[1:]-((edges[1]-edges[0])/2)), 
                region_depths[region_name][j] + region_counts[region_name][j], 
                linewidth=0.75)
        ax.set_title('Probe{} - {} PSTH'.format(probe_name[-1], region_name))
        ax.set_ylabel('Depth')
        ax.axvspan(-0.2,0,color='gray',alpha=0.2);
        ax.set_xlim([-100, 250])
        ax.set_xlabel('Time (msec)')
        fig.savefig(os.path.normpath('D:\\Images\\AvgOverImages\\' + 'Probe{}_{}_PSTH.png'.format(probe_name[-1], region_name)))
        

# Heat map
for i, region_name in enumerate(all_regions):
    fig_name = 'Probe{}_{}'.format(probe_name[-1], region_name)
    fig, ax = plt.subplots(1, 1, figsize=(10,10))
    ax.imshow(np.vstack(region_counts[region_name]))
    ax.set_title('Probe{} - {} PSTH'.format(probe_name[-1], region_name))
    fig.savefig(os.path.normpath('D:\\Images\\AvgOverImages\\' + fig_name + '_psth.png'))
