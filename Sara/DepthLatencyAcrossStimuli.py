# -*- coding: utf-8 -*-
"""
Latency-depth across stimuli

Created on Thu Aug 30 10:04:25 2018

@author: sarap
"""
import os
import sys
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt

#%%
latency_path = os.path.normpath('d:/Latencies/')
sys.path.append('d:/resources/mindreading/sara')
from neuropixel_data import load_depth_df
from neuropixel_plots import region_color
from cortical_layers import plot_units_by_depth, latency_by_depth

#%%
region_list = {'VISpm', 'VISam', 'VISp', 'VISl', 'VISal', 'VISrl', 'TH', 'SCs', 'DG', 'CA'}
expt_index = 58
stim_list = ['natural_scenes', 'static_gratings','drifting_gratings']

for region in region_list:
    
    fig, ax = plt.subplots(2, 1, figsize=(6,8), gridspec_kw={'height_ratios': [1, 3]})
    ax = ax.flatten()
    stim_dict = {}
    for stim in stim_list:
        depth_df = load_depth_df(expt_index, stim, region)
        ax[1], _ = latency_by_depth(depth_df, show_data=False, ax=ax[1], label=stim)
        x = depth_df.groupby('depth').count()
        # ax[0] = plot_units_by_depth(depth_df, ax=ax[0], color=region_color(region, light=True))
    ax[0].plot(x.index, x['unit_id'], color=region_color(region, light=True), linewidth=3)
    ax[1].legend(fontsize=15)
    ax[1].set_ylim(0,150)
    # ax[0].set_xlim(ax[1].get_xlim())
    ax[0].set_title('{} Latencies by Depth ({})'.format(region, expt_index))
    ax[1].set_xlim(ax[0].get_xlim())
    ax[0].get_xaxis().set_visible(False)
    fig.savefig(os.path.join(latency_path, '{}_{}_latency_depth.png'.format(expt_index, region)))

#%%
region_list = {'VISp', 'VISam', 'VISpm', 'VISl', 'VISrl'}
stim_list = ['natural_scenes', 'static_gratings','drifting_gratings']

for region in region_list:
    fig, ax = plt.subplots()
    stim_dict = {}
    for stim in stim_list:
        depth_df = load_depth_df(10, stim, region)
        ax, stim_dict = latency_by_depth(depth_df, show_data=False, ax=ax, label=stim.replace('_', ' '))
    ax.set_title('{} Response Latencies (10)'.format(region))
    ax.legend(fontsize=16)
    ax.set_ylim(0,200)
    fig.savefig(os.path.join(os.path.normpath('d:/depths'), '{}_{}_depthlatency.png'.format(10, region)))