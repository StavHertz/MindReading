# -*- coding: utf-8 -*-
"""
Iterate through natural scenes and create PSTH and heatmap of all responses for
a single probe.

Created on Fri Aug 24 14:00:39 2018

@author: sarap
"""

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
print multi_probe_filename
nwb_file = os.path.join(drive_path, multi_probe_filename)

data_set = NWB_adapter(nwb_file)
probe_spikes = data_set.spike_times[probe_name]

ns_table = data_set.get_stimulus_table('natural_scenes')

for image_id in np.unique(ns_table['frame']):
    
    fig_name = 'Probe{}_Image {}'.format(probe_name[-1], image_id)

    frame_table = ns_table[ns_table.frame == image_id]

    all_trains = {}
    probe_units = data_set.unit_df[(data_set.unit_df['probe']==probe_name)]
    unit_list = probe_units['unit_id'].values

    for i, unit_row in probe_units.iterrows():
    	spike_train = probe_spikes[unit_row['unit_id']]
    	stim_train = []
    	for ind, stim_row in frame_table.iterrows():
            current_train = spike_train[(spike_train > stim_row['start'] - pre_stimulus_time) & (spike_train <= stim_row['end'])] - stim_row['start']
            stim_train.append(current_train)
            all_trains[unit_row['unit_id']] = stim_train
    # Heat map
    fig,ax = plt.subplots(1,1,figsize=(15,20))
    plt.imshow(np.vstack(all_counts))
    fig_name = 'Probe{}_Image {}'.format(probe_name[-1], image_id)
    ax.set_title(fig_name)
    fig.savefig(os.path.normpath('D:\\Images\\' + fig_name + '_heatmap.png'))

    fig,ax = plt.subplots(1,1,figsize=(6,20))
    for i, unit_row in probe_units.iterrows():
    	counts, edges = np.histogram(np.hstack(all_trains[unit_row['unit_id']]), bins=bins)
    	plt.plot(edges[1:], unit_row['depth']+15*counts, linewidth=0.7)
    ax.set_ylabel('Depth')
    ax.axvspan(-0.2,0,color='gray',alpha=0.2);
    ax.set_xlim([-0.1, 0.25])
    ax.set_xlabel('Time (sec)')
    ax.set_title(fig_name)
    fig.savefig(os.path.normpath('D:\\Images\\' + fig_name + '_sdf.png'))	



