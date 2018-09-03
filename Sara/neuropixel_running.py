# -*- coding: utf-8 -*-
"""
Functions to analyze running speed data for neuropixel probe experiments

Created on Fri Aug 31 00:49:31 2018

@author: sarap
"""

import h5py
import numpy as np
import pandas as pd

SPEED_CUTOFF = 3  # cm/sec

def get_running_speed_by_frame(rtime, rspeed, frame_table):
    """
    Parameters
    ----------
    rtime : array-like
        Timestamps for running speed
    rspeed : array-like
        Running speeds (cm/s)
    frame_table : pandas.DataFrame
        Stimulus table
    """
    avg_speed = np.zeros_like(frame_table['start'].values)
    speed_binary = np.zeros_like(avg_speed)
    i = 0
    for j, row in frame_table.iterrows():
        ind = np.where((rtime >= row['start']) & (rtime < row['end']))
        stim_speed = rspeed[ind].astype(float)
        avg_speed[i] = np.mean(stim_speed)
        if np.mean(stim_speed) >= SPEED_CUTOFF:
            speed_binary[i] = 1
        else:
            speed_binary[i] = 0
        i += 1  # stim table indices are not sequential
    
    new_frame_table = frame_table.copy()
    new_frame_table['speed'] = avg_speed
    new_frame_table['running'] = speed_binary.astype(bool)
    return new_frame_table


def get_running_speed(dataset):
    """
    Parameters
    ----------
    dataset : NWB_adapter
        Dataset to extract running speeds from 
    
    Returns
    -------
    running_timestamps
    running_speed
    
    Notes
    -----
    Copied from Shawn's function in swdb_2018_tools
    """
    f = h5py.File(dataset.nwb_path, 'r') 
    
    try:
        running_speed = f['acquisition']['timeseries']['RunningSpeed']['data'].value
        running_timestamps = f['acquisition']['timeseries']['RunningSpeed']['timestamps'].value
    except:
        running_speed = []
        running_timestamps = []
        
    f.close()
    
    return running_timestamps, running_speed
