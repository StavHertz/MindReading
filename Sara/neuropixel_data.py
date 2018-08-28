# -*- coding: utf-8 -*-
"""
Utilities for loading and saving neuropixel probe data

Created on Sun Aug 26 16:12:53 2018

@author: sarap
"""
import os
import pickle
import pandas as pd
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter

def open_experiment(drive_path, expt_num=0, multi_probe=True):
    """
    Open a neuropixel probe experiment, return dataset object
    
    Parameters
    ----------
    drive_path : str
        Location of Allen Inst neuropixel probe datafiles
    multi_probe : optional, true
        Import multiprobe data (true) or single probe data (false)
    expt_num : optional, default = 0
        Experiment number to load
    
    Returns
    -------
    data_set : nwb_data
    """
    manifest_file = os.path.join(drive_path,'ephys_manifest.csv')
    expt_info_df = pd.read_csv(manifest_file)
    
    if multi_probe:
        expt_info_df = expt_info_df[expt_info_df.experiment_type == 'multi_probe']
    else:
        expt_info_df = expt_info_df[expt_info_df.experiment_type == 'single_probe']
    
    multi_probe_filename = expt_info_df.iloc[expt_num]['nwb_filename']
    nwb_file = os.path.join(drive_path, multi_probe_filename)
    print('Importing data file from {}'.format(nwb_file))

    # Import the data file
    data_set = NWB_adapter(nwb_file)
    
    # Print experiment info
    print('Regions: ', data_set.region_list)
    print('Neuropixel probes: ', data_set.probe_list)
    
    print('Full region list:')
    for probe in data_set.probe_list:
        probe_df = data_set.unit_df[data_set.unit_df['probe'] == probe]
        print(probe, probe_df['structure'].unique())
    
    return data_set


def open_gabor_analysis(exp_num, probe_name):
    """
    Load a Gabor RF mapping analysis file
    
    Parameters
    ----------
    exp_num : char
        Experiment number
    probe_name : char
        Which probe (A-F)
    
    Returns
    -------
    gabor_analysis : pandas.DataFrame
    """
    if int(exp_num) in [84, 10, 21, 58]:
        fname = '{}multi_probe{}.pkl'.format(str(exp_num), probe_name[-1])
    else:
        fname = '{}single_probe{}.pkl'.format(str(exp_num) probe_name[-1])
    
    if os.path.isfile(os.path.normpath(rf_path + '//' + fname)):
        gabor_analysis = pickle.load(open(fname))
    else:
        gabor_analysis = []
    return gabor_analysis
