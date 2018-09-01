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

rf_path = os.path.normpath('D:/RFMaps/')
latency_path = os.path.normpath('D:/Latencies/')

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


def check_folder(file_path):
    """
    Check if a folder exists, if not create a new one
    
    Parameters
    ----------
    file_path : str 
        New/existing folder path
    """
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        print('Created folder: {}'.format(file_path))


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
        fname = '{}single_probe{}.pkl'.format(str(exp_num), probe_name[-1])
    
    if os.path.isfile(os.path.normpath(rf_path + '//' + fname)):
        gabor_analysis = pickle.load(open(fname))
    else:
        gabor_analysis = []
    return gabor_analysis


def load_depth_df(expt_index, stim_name, region, json=False):
    """
    Parameters
    ----------
    expt_index : int
        Experiment index
    stim_name : char
        Stimulus name
    region : char
        Brain region
    json : optional, bool
        Load .json (default = false, loads as .pkl)
    
    Returns
    -------
    pandas.DataFrame
    """
    
    fpath = os.path.join(latency_path, str(expt_index), '{}_{}_latency'.format(region, stim_name))
    if json:
        if not os.path.exists(fpath + '.json'):
            print('No .json file found for {}-{}-{}'.format(expt_index, region, stim_name))
            return
        raise NotImplementedError('feeling lazy..')
    else:
        if not os.path.exists(fpath + '.pkl'):
            print('No .pkl file found for {}-{}-{}'.format(expt_index, region, stim_name))
            return
        f = open(fpath+'.pkl')
        depth_df = pickle.load(f)
        f.close()
    return depth_df
    

def get_depth(dataset, probe_name):
    """
    Get a dictionary with units as keys and electrode depth as values
    
    Parameters
    ----------
    dataset : NWB dataset
        Neuropixel dataset
    probe_name : str
        Which probe
    
    Return
    ------
    depths : dict
    """
    unit_df = dataset.unit_df[dataset.unit_df['probe'] == probe_name]
    depths = {}
    for i, row in unit_df.iterrows():
        depths[row['unit_id']] = row['depth']
    
    return depths


def split_latency_df(latency_dict, exp_index):
    """
    Conversion for output of Sebastien's latency analysis code
    
    Parameters
    ----------
    latency_dict : dict
        Latency dictionary containing dataframes per stimulus
    exp_index : str
        Experiment number
    """
    save_path = os.path.join(latency_path, str(exp_index))
    check_folder(save_path)
    for stim in latency_dict.keys():
        stim_df = latency_dict[stim]
        for region in stim_df['region'].unique():
            region_df = stim_df[stim_df['region'] == region]
            fname = os.path.join(save_path, '{}_{}_latency'.format(region, stim))
            # Save as .pkl file
            print('Saving as: {}'.format(fname))
            f = open(fname + '.pkl', 'wb')
            pickle.dump(region_df, f)
            f.close()
            
            # Also .json for now
            region_df.to_json(fname + '.json', orient='split')
            
            
        
    
