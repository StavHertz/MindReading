# -*- coding: utf-8 -*-
"""
Plotting functions for neuropixel probe data

Created on Sat Aug 25 09:08:57 2018

@author: sarap
"""

import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set_context('notebook', font_scale=1.4)

__all__ = ['probe_heatmap', 'image_raster', 'image_psth', 'get_psth', 
           'get_avg_psth', 'plot_psth']

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


def get_psth(stim_df, unit_spikes, pre_time=.1, tail_time=0, bin_width=0.005):
    """
    Parameters
    ----------
    stim_df : pandas.DataFrame
        Stimulus table, will be averaged together
    unit_spikes : list
        Spike times for one unit
    pre_time : optional, default = .1 (seconds)
        Time before stimulus to include in PSTH
    tail_time : optional, default = 0
        Time after stimulus presentation to include in PSTH
    bin_width : optional, 0.005 milliseconds
        Bin size
    
    Returns
    -------
    mean_fr : average PSTH (spikes/sec)
    centers : centers of PSTH time bins
    """

    all_trials = []
    for i, start in enumerate(stim_df.start):
        trial_spikes = unit_spikes[(unit_spikes > start-pre_time) & (unit_spikes < stim_df['end'].values[i]+tail_time)]       
        trial_spikes = trial_spikes - start
        all_trials.append(list(trial_spikes))
    
    #for i, stim_row in stim_df.iterrows():
    #    trial_spikes = unit_spikes[(unit_spikes > stim_row['start']-pre_time) & (unit_spikes < stim_row['end']+tail_time)]
    
    # Make PSTH for each trial
    total_time = (stim_df['end'].values[0] - stim_df['start'].values[0]) + tail_time
    bins = np.arange(-pre_time,total_time+bin_width,bin_width)
    fr_per_trial = []
    for trial_spikes in all_trials:
        counts, edges = np.histogram(trial_spikes, bins)
        counts = counts/bin_width
        fr_per_trial.append(counts)
    centers = edges[:-1] + np.diff(edges)/2
    
    return fr_per_trial, centers


def get_avg_psth(stim_df, unit_spikes, pre_time=.1, tail_time=0, showme=False):
    """
    Parameters
    ----------
    stim_df : pandas.DataFrame
        Stimulus table, will be averaged together
    unit_spikes : list
        Spike times for one unit
    pre_time : optional, default = .1 (seconds)
        Time before stimulus to include in PSTH
    tail_time : optional, default = 0
        Time after stimulus presentation to include in PSTH
    showme : optional, False
        Plot the output
    
    Returns
    -------
    mean_fr : average PSTH (spikes/sec)
    centers : centers of PSTH time bins
    """
    fr_per_trial, centers = get_psth(stim_df, unit_spikes, pre_time, tail_time)
    mean_fr = np.mean(fr_per_trial, axis=0)
    if showme:
        plot_psth(mean_fr, centers)
    return mean_fr, centers


def plot_psth(psth, centers, ax=[]):
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
