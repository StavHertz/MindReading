#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 17:09:23 2018

@author: rahulbiswas
"""

def get_highfire_starts(sdf,pre_stim_time,min_start_time):#final
    '''
    This function estimates and returns the first time (in miliseconds) the neuron starts high-firing.
    Input : An array with spike density function values over each milisecond,
            Time (in seconds) until stimulus onset,
            Minimum latency (in seconds) after stimulus onset
    Output : Index in sdf array where high-firing after stimulus starts
    '''
    from find_min_highfire import find_min_highfire
    import numpy as np
    import scipy.stats as stats
    from scipy.signal import argrelextrema
    from scipy.stats import iqr
    #get data stimulus and a minimum duration of baseline
    sdf_stim=sdf[(int(1000*(pre_stim_time))+min_start_time):]
    sdf_max_idx=np.argmax(sdf_stim)
    baseline = sdf[(int(1000*(pre_stim_time))-15):(int(1000*(pre_stim_time))+15)]
    if np.mean(baseline)==0:#check if no positive sdf in baseline
        return np.nan
    
    #determine threshold
    thresh00=np.percentile(baseline,50)*np.exp(25*stats.variation(np.abs(baseline))*iqr(np.log(np.abs(baseline))))
    sdf_max_idx_all=argrelextrema(sdf_stim, np.greater_equal,order=2)[0]
    thresh01=thresh00;
    thresh0 = 0.5*(thresh00+thresh01)

    #check if threshold is nan. this can happen if baseline values too low for np.log to return a number
    if np.isnan(thresh0):
        return np.nan
    if len(sdf_max_idx_all)==0:# check if no local maxima found in considered duration of sdf
        out_idx = np.nan
    else:
        if np.all(sdf_stim[sdf_max_idx_all]<thresh0):#check if none of the peaks are higher than threshold
            out_idx = np.nan
        else:
            sdf_stim_subset=sdf_stim[:sdf_max_idx];out_idx=sdf_max_idx;
            while True:#roll the ball to troughs before the highest peak conditional on statistical significance
                if len(sdf_stim_subset)<3:
                    break;
                else:
                    if out_idx-find_min_highfire(sdf_stim_subset)>=75:
                        break
                    out_idx=find_min_highfire(sdf_stim_subset);
                    sdf_stim_subset2 = sdf_stim[:out_idx];
                    thresh=np.percentile(sdf_stim_subset2,75)#checking if trough is in the 75 percentile band based on sdf before it.
                    if sdf_stim_subset[out_idx]<thresh:
                        break;
                    else:
                        sdf_max_idx2_all=argrelextrema(sdf_stim_subset2, np.greater_equal,order=2)[0]
                        if len(sdf_max_idx2_all)==0:
                            break;
                        sdf_max_idx2=sdf_max_idx2_all[-1]
                        sdf_stim_subset2=sdf_stim_subset[:sdf_max_idx2]
                        sdf_stim_subset=sdf_stim_subset2;
        if not np.isnan(out_idx):
            #get the index in the middle of the detected starting trough and immediate next peak for greater accuracy
            idx_temp=argrelextrema(sdf_stim[out_idx:],np.greater_equal,order=2)[0][0]
            out_idx=out_idx+(idx_temp/2);
            out_idx=out_idx+min_start_time;#adjust for the minimum baseline time not considered
    #####negative side -- adapting the same algorithm above for negative sdf
    sdf_stim=-sdf[(int(1000*(pre_stim_time))+min_start_time):]
    sdf_max_idx=np.argmax(sdf_stim)
    baseline = -sdf[(int(1000*(pre_stim_time))-20):(int(1000*(pre_stim_time))+20)]
    thresh00=np.percentile(baseline,50)*np.exp(-25*stats.variation(np.abs(baseline))*iqr(np.log(np.abs(baseline))))
    sdf_max_idx_all=argrelextrema(sdf_stim, np.greater_equal,order=2)[0]
    thresh01=thresh00;
    thresh0 = 0.5*(thresh00+thresh01)
    if np.isnan(thresh0):
        return np.nan
    if len(sdf_max_idx_all)==0:
        out_idx2=out_idx;
    else:
        if np.all(sdf_stim[sdf_max_idx_all]<thresh0):
            out_idx2=out_idx;
        else:
            sdf_stim_subset=sdf_stim[:sdf_max_idx];out_idx2=sdf_max_idx;
            while True:
                if len(sdf_stim_subset)<3:
                    break;
                else:
                    if out_idx2-find_min_highfire(sdf_stim_subset)>=75:
                        break
                    out_idx2=find_min_highfire(sdf_stim_subset);
                    sdf_stim_subset2 = sdf_stim[:out_idx2];
                    thresh=np.percentile(sdf_stim_subset2,75)
                    if sdf_stim_subset[out_idx2]<thresh:
                        break;
                    else:
                        sdf_max_idx2_all=argrelextrema(sdf_stim_subset2, np.greater_equal,order=2)[0]
                        if len(sdf_max_idx2_all)==0:
                            break;
                        sdf_max_idx2=sdf_max_idx2_all[-1]
                        sdf_stim_subset2=sdf_stim_subset[:sdf_max_idx2]
                        sdf_stim_subset=sdf_stim_subset2;
        
        if not np.isnan(out_idx2):
            idx_temp=argrelextrema(sdf_stim[out_idx2:],np.greater_equal,order=2)[0][0]
            out_idx2=out_idx2+(idx_temp/2);
            out_idx2=out_idx2+min_start_time;
    l1=out_idx
    l2=out_idx2
    
    #choosing between detections from the positive and negative sdf
    if np.isnan(l1) and np.isnan(l2):
        return np.nan
    elif np.isnan(l1) and ~np.isnan(l2):
        return l2
    elif np.isnan(l2) and ~np.isnan(l1):
        return l1
    else:
        return np.min([l1,l2])