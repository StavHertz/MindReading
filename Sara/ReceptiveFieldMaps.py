# -*- coding: utf-8 -*-
"""
Code for generating final receptive fields used in presentation

See GaborReceptiveFieldDemos.py for the individual RFs 

Created on Thu Aug 30 14:38:24 2018

@author: sarap
"""


#%% IMPORTS
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
sns.set_palette('deep')
sns.plotting_context(rc={'font.size': 18})

#%% SPECIFIC IMPORTS
sys.path.append('d:/resources/mindreading/sara')
from neuropixel_plots import probe_heatmap, region_cmap, receptive_field_map
from neuropixel_spikes import get_avg_psth
from neuropixel_data import open_experiment

#%% SET PATHS
drive_path = os.path.normpath('d:/visual_coding_neuropixels')
rf_path = os.path.normpath('d:/RFMaps/')

#%% IMPORT DATA IF NEEDED
drive_path = os.path.normpath('d:/visual_coding_neuropixels/')
dataset = open_experiment(drive_path, 3)

#%% REGISTER PATH
expt_index = dataset.nwb_path[-6:-4]
print('Current experiment index: {}'.format(expt_index))

#%% STIMULUS SETTINGS
try:
    gabors = dataset.get_stimulus_table('gabor_20_deg_250ms')
except:
    gabors = dataset.get_stimulus_table('gabor_20_deg')

x_list = np.unique(gabors['pos_x'])
y_list = np.unique(gabors['pos_y'])
ori_list = np.unique(gabors['orientation'])
print('Tested {} XY positions'.format(len(x_list)*len(y_list)))
#%% SET PROBE
probe_list = dataset.probe_list
print('Neuropixel probes: ', probe_list)
# Get probe-specific stuff
for probe_name in probe_list:
    # PROBE-SPECIFIC VARIABLES
    probe_df = dataset.unit_df[dataset.unit_df['probe'] == probe_name]
    probe_spikes = dataset.spike_times[probe_name]
    # Get all neurons recorded
    unit_list = probe_spikes.keys()
    
    # Remove the noise unit, if needed
    if 'noise' in unit_list:
        unit_list.remove('noise')
    
    # Remove non-matching units
    print('Removing {} of {} units'.format(len(unit_list) - len(np.intersect1d(unit_list, probe_df['unit_id'])), len(unit_list)))
    unit_list = np.intersect1d(unit_list, probe_df['unit_id'])
    # Remove these from the probe data frame as well
    probe_df = probe_df[probe_df['unit_id'].isin(unit_list)]
    print('{} units on {}'.format(len(unit_list), probe_name))
    
    # Get all the regions recorded
    region_list = probe_df['structure'].unique()
    print('{} regions: '.format(len(region_list)), region_list)
    
    # AVERAGE PSTHs 
    # Calculated each unique combination of x, y and orientation
    # Or load pre-calculated from an existing .pkl file
    file_name = os.path.join(rf_path, '{}_{}_gabor_rf.pkl'.format(expt_index, probe_name))
    if os.path.exists(file_name):
        data = pickle.load(open(file_name))
        print('Loaded from {}'.format(file_name))
        save_flag = False
    else:
        data = []
        for unit in unit_list:
            unit_spikes = probe_spikes[unit]
            region_name = probe_df[probe_df['unit_id']==unit]['structure'].values[0]
            for i, x in enumerate(x_list):
                for j, y in enumerate(y_list):
                    for k, t in enumerate(ori_list):
                        tmp_df = gabors[(gabors['pos_x']==x) & (gabors['pos_y']==y) & (gabors['orientation']==t)]
                        psth, centers = get_avg_psth(tmp_df, unit_spikes)
                        resp = np.sum(psth[centers > 0])
                        ind = str(i) + str(j) + str(k)
                        data.append([ind, unit, region_name, x, y, t, psth, resp])
        gabor_analysis = pd.DataFrame(data, columns=['stim_id', 'unit_id', 'structure', 'x', 'y', 't', 'psth', 'resp'])
        save_flag = True  # Save the output
    
    # SAVE
    if save_flag:
        print('Saving as: {}'.format(file_name))
        f = open(file_name, 'wb')
        pickle.dump(gabor_analysis, f)
        f.close()
    
    # RECEPTIVE FIELD MAPS
    # Init empty map (orientation * x * y)
    rf_map = np.finfo(float).eps + np.zeros(shape=[3, len(x_list), len(y_list)])
    
    # Map per region
    for region in region_list:
        region_analysis = gabor_analysis[gabor_analysis['structure'] == region]
        for i, x in enumerate(x_list):
            for j, y in enumerate(y_list):
                for k, t in enumerate(ori_list):
                    ind = np.where(region_analysis['stim_id'] == str(i)+str(j)+str(k))
                    rf_map[k, i, j] = np.mean(region_analysis['resp'].values[ind])
        if rf_map.max() == 0:
            continue
        # Normalize receptive fields by the maximum value
        norm_map = rf_map/rf_map.max()
        
        # Average RF per orientation
        fig, ax = receptive_field_map(norm_map, cmap=region_cmap(region))
        ax[1].set_title('{} on Probe{} ({})'.format(region, probe_name[-1], expt_index), fontsize=30)
        fig.savefig(os.path.normpath('{}\\{}{}_{}_mean_oriented_gabor.png'.format(rf_path, expt_index, probe_name, region)))
        
        # Single average RF
        fig, ax = receptive_field_map(np.mean(norm_map, axis=0), cmap=region_cmap(region))
        ax.set_title('{} Probe{} ({})'.format(region, probe_name[-1], expt_index), fontsize=26)
        fig.savefig(os.path.normpath('{}\\{}{}_{}_mean_oriented_gabor.png'.format(rf_path, expt_index, probe_name, region)))
