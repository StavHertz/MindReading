# -*- coding: utf-8 -*-
"""
Latency-depth across stimuli

Created on Thu Aug 30 10:04:25 2018

@author: sarap
"""
import os
import sys
import scipy.signal
from scipy.stats import binned_statistic
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('talk', font_scale=1.4, rc={'lines.markeredgewidth': 2})
sns.plotting_context(rc={'font.size': 18})
sns.set_style('whitegrid')
sns.set_palette('deep');

#%%
latency_path = os.path.normpath('d:/Latencies/')
sys.path.append('d:/resources/mindreading/sara')
from neuropixel_data import load_depth_df
from neuropixel_plots import region_color, rgb2hex, stim_color
from cortical_layers import plot_units_by_depth, latency_by_depth

#%% Function
def latency_depth_binstat(depth_df, color='k',shade=None, bin_size=50, ax=[]):
    """
    Parameters
    ----------
    depth_df : pandas.DataFrame
        Containing depth and latency columns
    bin_size : optional, int
        Size of depth bins in microns
    """
    
    if not ax:
        fig, ax = plt.subplots()
    
    if shade is None:
        shade = sns.desaturate([0, 0, 1], 0.2)
    
    depths = depth_df['depth'].values
    depths = depths[depth_df['latency'].notna()]
    latencies = depth_df['latency'].values
    latencies = latencies[depth_df['latency'].notna()]
    depths = depths.astype(float)
    latencies = latencies.astype(float)
    
    bins = np.arange(depths.min(), depths.max(), bin_size)
    bin_centers = bins[:-1] - (np.abs(bins[1]-bins[0]))/2
    
    x, _, _ = binned_statistic(depths, latencies, 'mean', bins=bins)
    x_sem, _, _ = binned_statistic(depths, latencies, statistic=sem, bins=bins)
    
    ind = np.where((x > 2) & (x < 190))
    x = x[ind]
    x_sem = x_sem[ind]
    bin_centers = bin_centers[ind]
    
    ax.errorbar(bin_centers, x, color=color, linewidth=3)
    ax.fill_between(bin_centers, x-x_sem, x+x_sem, color=shade, alpha=0.3)
    ax.set_ylim(0,)
    
    return ax


def sem(x):
    """
    Calculate standard error of the mean
    
    x : array-like
    """
    y = np.std(x)/np.sqrt(len(x))
    return y


#%%
region_list = {'VISpm', 'VISam', 'VISp', 'VISl', 'VISal', 'VISrl', 'TH', 'SCs', 'DG', 'CA'}
expt_index = 10
stim_list = ['natural_scenes', 'static_gratings']

for region in region_list:
    
    fig, ax = plt.subplots(2, 1, figsize=(6,8), gridspec_kw={'height_ratios': [1, 3]})
    ax = ax.flatten()
    stim_dict = {}
    for stim in stim_list:
        depth_df = load_depth_df(expt_index, stim, region)
        ax[1], stim_dict[stim] = latency_by_depth(depth_df, show_data=False, ax=ax[1], label=stim)
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

region_list = {'VISpm', 'VISam', 'VISp', 'VISl', 'VISal', 'VISrl', 'TH', 'SCs', 'DG', 'CA'}
expt_index = 10
stim_list = ['natural_scenes', 'static_gratings']

for region in region_list:
    fig, ax = plt.subplots(1,1,figsize=(4,8))
    for stim in stim_list:
        depth_df = load_depth_df(expt_index, stim, region)
        try:
            ax = latency_depth_binstat(depth_df, ax=ax, bin_size=50, shade=stim_color(stim)[2][:-1], color=stim_color(stim)[-1][:-1])
        except:
            print('{}-{} did not plot'.format(expt_index, stim))
    ax.set_xlabel('Depth (um)')
    ax.set_ylabel('Latency (ms)')
    ax.set_ylim(0,200)
    ax.set_title('{} Layers by Latency ({})'.format(region, expt_index))
    fig.subplots_adjust(bottom=0.5)
    fig.savefig(os.path.join(latency_path, '{}_{}_depthlatency_goodhist.png'.format(expt_index, region)), dpi=600)