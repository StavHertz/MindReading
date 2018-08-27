# -*- coding: utf-8 -*-
"""
Collection of functions for analysis of spikes from neuropixel probes

Created on Sun Aug 26 15:33:52 2018

@author: sarap
"""

import numpy as np

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
