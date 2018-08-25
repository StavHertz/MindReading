#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 22:56:37 2018

@author: maximechevee1

MC's attempt at plotting the PSTHs from the neuropixel data
"""

drive_path = '/Users/maximechevee1/Documents/SWDB_2018/visual_coding_neuropixels'
drive_path

# We need to import these modules to get started
import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

#define a few useful functions
def get_units_in_visual_cortex(cortical_region_name, data_set):
    '''Inputs:
            cortical_region_name: the name of visual cortical region ('VISp','VISl','VISal','VISrl','VISam','VISpm')
            data_set: data_set object for one ephys experiment
       Returns:
            vis_unit_list: list of unit_IDs in the cortical region '''
    
    # Select dataframe subset of units in cortical region
    subset_unit_df = data_set.unit_df[data_set.unit_df['structure']==cortical_region_name]
    
    # Make a list of unit_ids that are in visual cortical region on specified probe
    vis_unit_list = list(subset_unit_df['unit_id'].values)
    
    return vis_unit_list

def image_raster(img,unit_spikes,ax):
    
    #Default params
    if not ax:
        fig,ax = plt.subplots(1,1,figsize=(6,3))

    pre_time = .1
    post_time = .25

    all_trials = []
    # Get spike train for each trial and append to all_trials
    for i,start in enumerate(img.start):
        spikes = unit_spikes[(unit_spikes > start-pre_time) & (unit_spikes < start+post_time)]
        spikes = spikes - start
        all_trials.append(list(spikes))

    # Plot raster for each trial
    for i,spikes in enumerate(all_trials):
        ax.plot(spikes,i*np.ones_like(spikes),'|',color='b',markersize=4)
        ax.invert_yaxis()  
    
    ax.axvspan(0,0.25,color='gray',alpha=0.2);
    return ax


# Provide path to manifest file
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')

# Create a dataframe 
expt_info_df = pd.read_csv(manifest_file)

# Display information contained in the dataframe
expt_info_df

#Make Dataframe containing multielectrode experiements
multi_probe_expt_info=expt_info_df[expt_info_df.experiment_type=='multi_probe']
multi_probe_expt_info
print(len(multi_probe_expt_info))

#import the NWB_adapter to be able to process the neuropixel dataframe
sys.path.append('/Users/maximechevee1/Documents/SWDB_2018/neuropixels_repo')
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter

#Get a single example experiment and create the NWB object
multiprobe_example=1
multiprobe_filename=multi_probe_expt_info.iloc[multiprobe_example]['nwb_filename']

sys.path.append('/Users/maximechevee1/Documents/SWDB_2018/neuropixels_repo')
nwb_file = os.path.join(drive_path,multiprobe_filename)

data_set = NWB_adapter(nwb_file)



#Strategy: get the spikes and stims time stamps for one cell, then split by trials and align

## Get spikes for example unit

#from the data_set (datafranme), get the spikes from your favorite structure
v1_unit_df = data_set.unit_df[data_set.unit_df['structure']=='VISp']

#from the data_set (dataframe), get the spikes from your favorite probe
probe_spikes = data_set.spike_times['probeC']

#get the spikes in visual cortex
vis_unit_list=get_units_in_visual_cortex('VISp', data_set) #list
example='267'
unit_spikes= probe_spikes[example]

#make the img object, which has the start times for each stimulus
dg_stim_full = data_set.get_stimulus_table('drifting_gratings')
dg_stim_full.head()

def kernel_fn(x,h):
    return (1./h)*(np.exp(1)**(-(x**2)/h**2))

def get_sdf_from_spike_train(spike_train,h=None):
    n=len(spike_train)
    sdf=np.zeros(n);
    out=np.abs(np.mgrid[0:n,0:n][0]-np.matrix.transpose(np.mgrid[0:n,0:n][0]))
    sdf=1000*np.mean(kernel_fn(out,h)*spike_train,axis=1)
    return sdf

# Plot raster for each trial
from scipy.stats.kde import gaussian_kde
from scipy.stats import norm


#test for one orientation
pre_time = .1
post_time = .25
sampling_rate=30000 #per second

for m,orientation in enumerate(np.unique(dg_stim_full.orientation)[~np.isnan(np.unique(dg_stim_full.orientation))]):
    dg_stim_90=dg_stim_full[dg_stim_full.orientation==orientation]
    all_trials = []
            plt.figure()
        # Get spike train for each trial and append to all_trials
    for i,start in enumerate(dg_stim_90.start):
        spikes = unit_spikes[(unit_spikes > start-pre_time) & (unit_spikes < start+post_time)]
        spikes = spikes - start
        all_trials.append(list(spikes))
        #sdf_unit=np.zeros((len(all_trials),int((post_time+pre_time) *sampling_rate)))
    for i,trial in enumerate(all_trials):
        #temp=np.zeros(int((post_time+pre_time) *sampling_rate))
        plt.plot(trial,i*np.ones_like(trial),'|',color='b',markersize=4)
        plt.axvspan(0,0.25,color='gray',alpha=0.2);
    
    #    for j, spike in enumerate(trial):
    #        temp[int(spike*sampling_rate)]=1
    #    
    #    if sum(temp)==0:
    #        temp_sdf=temp
    #    else:
    #        temp_sdf=get_sdf_from_spike_train(temp, h=10)
    #
    #    sdf_unit[i,:]=temp_sdf
    
    
#    mean_sdf_unit=np.mean(sdf_unit, axis=0)
#    plt.plot(np.arange(len(temp)), mean_sdf_unit)        
#    
    
