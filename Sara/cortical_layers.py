"""
Cortical layer analysis and plotting

Created on Wed Aug 30 23:12:53 2018

@author: sarap
"""

import os
import pandas as pd
import numpy as np 
import scipy.signal 

import matplotlib.pyplot as plt 
import seaborn as sns
sns.set_context('talk', font_scale=1.6, rc={'lines.markeredgewidth': 2})
sns.plotting_context(rc={'font.size': 18})
sns.set_style('white')
sns.set_palette('deep')

def units_by_depth(depth_df):
    """
    Get a list of the number of units at each depth. 
    Responsivity is not taken into account

    Parameters
    ----------
    depth_df : pandas.DataFrame
        Depth Analysis dataframe (contains 'depth' column)
    
    Returns
    -------
    depths : each unique depth
    counts : number of units at each value in depths
    """

    s = depth_df['depth'].value_counts()
    s.sort_index(ascending=False)
    return s.index, s.values


def plot_units_by_depth(depth_df, ax=[], save_path=[]):
    """
    Parameters
    ----------
    depth_df : pandas.DataFrame
        Latency dataframe
    ax : optional, matplotlib axis handle
        Axis to plot to (default = new axis)
    Returns
    -------
    ax : axis handle
    """
    if not ax:
        ax = sns.countplot(x='depth', data=depth_df)
    else:
        sns.countplot(x='depth', data=depth_df, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_xlabel('Depth (um)')
    ax.set_ylabel('Number of units')

    if save_path:
        fig = ax.figure()
        fig.savefig(save_path)

    return ax

def plot_latency_by_depth(depth_df, show_data=False, save_path=[], ax=[]):
    
    if not ax:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    
    _, depth_dict = latency_by_depth(depth_df)
    
    ax.plot(depth_dict['smooth_depth'], depth_dict['smooth_latency'], linewidth=3)
    # Plot raw data points
    ax.plot(depth_dict['latency'], depth_dict['depth'], marker='o', linestyle='none', alpha=0.2, color='k')
    ax.set_ylim(0,)
    ax.set_xlabel('Depth (um)')
    ax.set_ylabel('Latency (ms)')
    fig.savefig(save_path + '_smooth.png')


def latency_by_depth(depth_df, sg_window=5, sg_bins=20, sg_order=2, use_median=False, ax=[], show_data=True, label=[]):
    """
    Parameters
    ----------
    depth_df : pandas.DataFrame
        LatencyAnalysis dataframe with 'depth' and 'latency'
    sg_window : optional, int
        Points for Savitsky-Golay window (default = 5)
    sg_order : optional, int
        Polynomial for Savitsky-Golay window (default = 2)
    sg_bins : optional, int
        Number of bins to divide data (default = 20)
    use_median : optional, bool
        Use median instead of mean (default = False)
    ax : optional, matplotlib axis handle
        Axis to plot to (default = new axis)
    show_data : optional, bool
        Plot raw data (default = True)
    label : optional, str
        Plot label for legend (default = [])
    
    Returns
    -------
    ax : matplotlib axes
    foo : dictionary of depths, latencies and smoothed/binned plotted values
    """

    # Clip out the NaNs
    depths = depth_df['depth'].values
    latencies = depth_df['latency'].values 
    depths = depths[depth_df['latency'].notna()]
    latencies = latencies[depth_df['latency'].notna()]
    
    # Remove latencies beyond 250 ms (only important for drifting grating)
    ind = np.where(latencies < 250)
    if len(ind) is not len(latencies):
        print('{} of {} latencies over 250 ms'.format(len(latencies)-len(ind[0]), len(latencies)))
    depths = depths[ind]
    latencies = latencies[ind]

    # Need at least as many data points as window for SG
    if len(latencies) < sg_window:
        print('Too few data points for smooth curve plot')
        return
    
    counts, edges = np.histogram(depth_df['depth'], bins=sg_bins)

    latency_metric = np.zeros_like(counts)
    for i in range(len(edges)-1):
        ind = np.where((depths >= edges[i]) & (depths < edges[i+1]))
        if use_median:
            latency_metric[i] = np.median(latencies[ind])
        else:
            latency_metric[i] = np.mean(latencies[ind])

    bin_centers = edges[:-1] - (edges[1]-edges[0])/2

    # Remove empty bins from final plot
    ind = np.where(latency_metric > 2)
    if len(ind[0]) < sg_window:
        print('Number of data points ({}) less than SG window ({})'.format(
            len(ind[0]), sg_window))
        return
    print('Bin size = {} ms'.format((np.max(edges)-np.min(edges))/sg_bins))

    x = bin_centers[ind]
    y = scipy.signal.savgol_filter(latency_metric[ind], sg_window, sg_order)

    if not ax:
        fig, ax = plt.subplots()
    
    ax.plot(x, y, linewidth=3, label=label)
    # Plot raw data points
    if show_data:
        ax.plot(depths, latencies, marker='o', linestyle='none', alpha=0.2, color='k')
    ax.set_ylim(0,)
    ax.set_xlabel('Depth (um)')
    ax.set_ylabel('Latency (ms)')
    
    foo = {}
    foo['smooth_depth'] = x
    foo['smooth_latency'] = y
    foo['depths'] = depths
    foo['latencies'] = latencies
    
    return ax, foo
