# -*- coding: utf-8 -*-
"""
Plotting functions for neuropixel probe data

Created on Sat Aug 25 09:08:57 2018

@author: sarap
"""
import os 
import sys 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set_context('notebook', font_scale=1.4)

__all__ = ['probe_heatmap', 'image_raster', 'image_psth', 'plot_psth',
           'receptive_field_map', 'depth_latency_map', 'region_color', 'rgb2hex']


def probe_heatmap(psth_matrix, depth, edges, pre_time):
	"""
	Parameters
	----------
	psth_matrix : np.array
		Matrix of PSTHs ([number of neurons x time])

	depths : list/np.array
		electrode depths corresponding to the rows of psth_matrix

	edges : list/np.array
		time bin edges returned by np.histogram in seconds

    Returns
    -------
    fig, ax : matplotlib figure handles
    
    Notes
    -----
    The time axis will be converted to milliseconds
	"""
	fig, ax = plt.subplots(1, 1, figsize=(15,20))
	bin_centers = edges[:-1]-(edges[1]-edges[0])/2

	# Plot the firing rate heatmap
	plt.imshow(psth_matrix, cmap='jet', interpolation='gaussian')
	# Add the stimulus onset, if necessary
	if pre_time > 0:
		ax.vlines(np.where(bin_centers == np.min(np.abs(bin_centers))), ax.get_ylim()[1], ax.get_ylim()[0], 'white', alpha=0.4)

	x_pts, y_pts = np.shape(psth_matrix)
	# Correct the x-axis (and convert to milliseconds)
	xfac = 1e3*((ax.get_xticks()/x_pts*np.max(bin_centers))-pre_time)
	ax.set_xticklabels([str(int(np.round(x))) for x in xfac])

	# Correct the y-axis
	yfac = ax.get_yticks()/y_pts*np.max(np.abs(depth))
	ax.set_yticklabels([str(int(-np.round(y))) for y in yfac])

	# Plot labels
	ax.set_xlabel('Time (ms)', fontsize=20)
	ax.set_ylabel('Depth (microns)', fontsize=20)

	return fig, ax


def image_raster(img, unit_spikes, ax):
    """
    Plot the raster for an image and unit
    
    Parameters
    ----------
    img : stimulus table for 1 image
    unit_spikes : spike times for 1 unit
    ax : axis handle
    """
    
    #Default params
    if not ax:
        fig,ax = plt.subplots(1,1,figsize=(6,3))

    pre_time = .5
    post_time = .75

    all_trials = []
    # Get spike train for each trial and append to all_trials
    for i, start in enumerate(img.start):
        # Extract spikes around stim time
        spikes_each_trial = unit_spikes[
            (unit_spikes > start-pre_time) &
            (unit_spikes <= start+post_time)]
        # Subtract start time of stimulus presentation
        spikes_each_trial = spikes_each_trial - start
        
        # Add spikes to the main list
        all_trials.append(list(spikes_each_trial))

    # Plot raster for each trial
    for i, tr_spikes in enumerate(all_trials):
        ax.plot(tr_spikes, i*np.ones_like(tr_spikes), '|', color='b')
        ax.invert_yaxis()      
    
    return ax


def plot_psth(psth, centers, ax=[]):
    """
    Plot a PSTH
    
    Parameters
    ----------
    psth : array_like
        Post-stimulus time histogram
    centers : array_like
        Bin centers
    ax : optional, matplotlib axis handle
    """
    if not ax:
        fig, ax = plt.subplots(1,1,figsize=(6,3))
    
    plt.plot(centers, psth)
    
    if np.min(centers) < 0:
        ax.axvspan(np.min(centers), 0, color='gray', alpha=0.2)
    ax.set_ylabel('Firing rate (Hz)', fontsize=16)
    ax.set_xlabel('Time (s)', fontsize=16)
    ax.set_xlim([np.min(centers), np.max(centers)])
    plt.show()
    
    return fig, ax


def receptive_field_map(rf_map, cmap=[]):
    """
    Map a single xy receptive field or a series of receptive fields
    
    Parameters
    ----------
    rf_map : np.array (x,y) or (t,x,y)
        Receptive field(s) 
    cmap : optional
        Colormap for figure
    
    Returns
    -------
    fig, ax : matplotlib handles
    """
    if not cmap:
        cmap = sns.cubehelix_palette(8, as_cmap=True)
        
    if rf_map.ndim == 2:
        fig, ax = plt.subplots(1, 1, figsize=(4, 4))
        sns.heatmap(rf_map, ax=ax, cmap=cmap, square=True, cbar=False, xticklabels=False, yticklabels=False)    
    elif rf_map.ndim > 2:
        fig, ax = plt.subplots(1, rf_map.shape[0], figsize=(12, 4))
        ax = ax.flatten()
        for i in range(rf_map.shape[0]):
            sns.heatmap(rf_map[i,:,:], ax=ax[i], square=True, cbar=False, xticklabels=False, yticklabels=False, cmap=cmap)
    
    return fig, ax
        

def image_psth(img, unit_spikes, ax=[]):
    """
    Parameters
    ----------
    img : stimulus table for one image
    unit_spikes : spike times for 1 unit
    ax : handle of matplotlib axes object
    
    Returns
    -------
    fig, ax : matplotlib object handles
    """
    
    #Default params
    if not ax:
        fig,ax = plt.subplots(1,1,figsize=(6,3))

    pre_time = 1.
    post_time = 1.

    all_trials = []
    # Get spike train for each trial
    for i, start in enumerate(img.start):
        trial_spikes = unit_spikes[(unit_spikes > start-pre_time) & (unit_spikes < start+post_time)]
        trial_spikes = trial_spikes - start
        all_trials.append(list(trial_spikes))

    # Make PSTH for each trial with 5 ms bins
    bin_width = 0.005  # 5 ms  
    bins = np.arange(-pre_time,post_time+bin_width,bin_width)
    fr_per_trial = []
    for trial_spikes in all_trials:
        counts, edges = np.histogram(trial_spikes, bins)
        counts = counts/bin_width
        fr_per_trial.append(counts)
    centers = edges[:-1] + np.diff(bins)/2
    
    mean_fr = np.mean(fr_per_trial, axis=0)
    
    # Plot mean PSTH across trials
    fig, ax = plt.subplots(1,1)
    plt.plot(centers, mean_fr)
    
    ax.axvspan(0,0.25,color='gray',alpha=0.1)
    ax.set_ylabel('Firing rate (spikes/second)')
    ax.set_xlabel('Time (s)')
    plt.show()   

    return fig, ax


def depth_latency_map(depth_df, save_path):
    """
    Parameters
    ----------
    depth_df : dataframe
        DataFrame from latency analysis
    save_path : optional, str
        If provided, figure will be saved as .png
    
    Returns
    -------
    g : seaborn.axisgrid.JointGrid
    """
    g = sns.jointplot(depth_df['latency'], depth_df['depth']*1e-3, kind='kde', space=0, stat_func=None, color=region_color(region))
    g.plot_marginals(sns.rugplot, height=0.12, color="k")
    g.set_axis_labels(xlabel='{} latency (ms)'.format(region), ylabel='{} depth (mm) '.format(region))
    if save_path is not None:
        g.savefig(save_path)
    return g


def region_cmap(region_name, rot=0.1, plotme=False):
    """
    Parameters
    ----------
    region_name : str
        Region abbreviation (VISp, TH, SCs, DG, etc)
    rot : float
    plotme : optional, bool
        plot colormap, default = false
    
    Returns
    -------
    cmap : seaborn colormap
    """
    
    starts = np.linspace(0.2, 2.8, 10)
    regions = ('VISam', 'VISpm', 'TH', 'SCs', 'DG', 'CA', 'VISp', 'VISl', 'VISal', 'VISrl')
    try:
        ind = regions.index(region_name)
        ind = starts[ind]
    except ValueError:
        print('Invalid Region {}. Accepted regions: '.format(region_name))
        print(regions)
        return
        
    cmap = sns.cubehelix_palette(start=ind, rot=rot, as_cmap=True)
    
    if plotme:
        sns.palplot(sns.cubehelix_palette(start=ind, rot=rot))
    return cmap


def region_color(region_name):
    """
    Parameters
    ----------
    region_name : str
        Structure recorded from
    
    Returns
    -------
    Hex color value for plotting
    """
    cmap = region_cmap(region_name)
    return rgb2hex(cmap.colors[-1])


def rgb2hex(rgb):
    """
    Convert an RGB value to hex
    
    Parameters
    ----------
    rgb : array_like
        Red, green, blue 
    """
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    
    if r+g+b < 3:
        r = int(r*255)
        g = int(g*255)
        b = int(b*255)
    hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    return hex
