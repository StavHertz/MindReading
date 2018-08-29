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
    from scipy.signal import argrelextrema
    ch=4.5;
    sdf_stim=sdf[(int(1000*(pre_stim_time))+min_start_time):]
    sdf_max_idx=np.argmax(sdf_stim)
    baseline = sdf[(int(1000*(pre_stim_time))-20):(int(1000*(pre_stim_time))+20)]
    if np.mean(baseline)==0:
        return np.nan
    thresh00=np.mean(baseline)*np.exp(ch*np.std(np.log(np.abs(baseline))))
    sdf_max_idx_all=argrelextrema(sdf_stim, np.greater_equal,order=2)[0]
    thresh01=thresh00;
    thresh0 = (thresh00+thresh01)/2
    if np.isnan(thresh0):
        return np.nan
    if len(sdf_max_idx_all)==0:
        out_idx = np.nan
    else:
        if np.all(sdf_stim[sdf_max_idx_all]<thresh0):
            out_idx = np.nan
        else:
            sdf_max_idx=np.min(sdf_max_idx_all[sdf_stim[sdf_max_idx_all]>=thresh0])

            sdf_stim_subset=sdf_stim[:sdf_max_idx];out_idx=0;
            while True:
                if len(sdf_stim_subset)<3:
                    break;
                else:
                    out_idx=find_min_highfire(sdf_stim_subset);
                    sdf_stim_subset2 = sdf_stim[:out_idx];
                    thresh=np.percentile(sdf_stim_subset2,75)
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
            idx_temp=argrelextrema(sdf_stim[out_idx:],np.greater_equal,order=2)[0][0]
            out_idx=out_idx+(idx_temp/2);
            out_idx=out_idx+min_start_time;
    #####negative side
    sdf_stim=-sdf[(int(1000*(pre_stim_time))+min_start_time):]
    sdf_max_idx=np.argmax(sdf_stim)
    baseline = sdf[(int(1000*(pre_stim_time))-20):(int(1000*(pre_stim_time))+20)]
    thresh00=np.mean(baseline)*np.exp(ch*np.std(np.log(baseline)))
    sdf_max_idx_all=argrelextrema(sdf_stim, np.greater_equal,order=2)[0]
    thresh01=thresh00;
    thresh0 = (thresh00+thresh01)/2
    if np.isnan(thresh0):
        return np.nan
    if len(sdf_max_idx_all)==0:
        out_idx2=out_idx;
    else:
        if np.all(-sdf_stim[sdf_max_idx_all]<thresh0):
            out_idx2=out_idx;
        else:
            sdf_max_idx=np.min(sdf_max_idx_all[-sdf_stim[sdf_max_idx_all]>=thresh0])

            sdf_stim_subset=sdf_stim[:sdf_max_idx];out_idx2=0;
            while True:
                if len(sdf_stim_subset)<3:
                    break;
                else:
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
    if np.isnan(l1) and np.isnan(l2):
        return np.nan
    elif np.isnan(l1) and ~np.isnan(l2):
        return l2
    elif np.isnan(l2) and ~np.isnan(l1):
        return l1
    else:
        if (l1==min_start_time and l2 > min_start_time) or (l2==min_start_time and l1 > min_start_time):
            return np.max([l1,l2])
        else:
            return np.min([l1,l2])