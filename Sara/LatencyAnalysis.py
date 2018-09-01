# -*- coding: utf-8 -*-
"""
Builds distribution of response onset times for each structure

Sara version of the latency analysis code
- Changes to speed, plotting, saving data

Created on Tue Aug 28 13:07:44 2018

@author: sarap44
"""

#%% STANDARD IMPORTS
import os
import sys
import time
import pickle
import numpy as np
import pandas as pd
import matplotlib.axes as plt_axes
import time

import matplotlib.pyplot as plt

import seaborn as sns
sns.set_context('talk', font_scale=1.6, rc={'lines.markeredgewidth': 2})
sns.plotting_context(rc={'font.size': 18})
sns.set_style('white')
sns.set_palette('deep')

#%% IMPORTS FROM MINDREADING REPOSITORY
sys.path.append('D:/resources/mindreading/Sara/')
from neuropixel_data import open_experiment, check_folder, get_depth

sys.path.append('D:/resources/mindreading/Sebastien/')
from SDF import SDF

#%% IMPORT DATA IF NEEDED
drive_path = os.path.normpath('d:/visual_coding_neuropixels/')
dataset = open_experiment(drive_path, 2)
#%% INFORMATION FOR SAVING
expt_index = dataset.nwb_path[-6:-4]
save_path = os.path.normpath('D:/Latencies/{}/'.format(expt_index))
print('Saving to: ', save_path)
check_folder(save_path)

#%% DATA SETTINGS

# Experiment to analyze:
stim_name = 'drifting_gratings'  # 'natural_scenes'
nice_stim_name = 'Drifting Gratings'  # 'Natural Scenes'
stim_table = dataset.get_stimulus_table(stim_name)
# stim_name = 'flash_decrement'
# stim_table = stim_table[stim_table['color'] == -1]
# Regions to analyze:
region_list = dataset.unit_df['structure'].unique()
print('Analyzing regions: ', region_list)

#%% ANALYSIS SETTINGS
pre_time = 100  # ms
post_time = 300  # ms

# Latency calculations
# Multiplier of standard errors for threshold detection
if stim_name is 'drifing_gratings':
    multiplier = 0.25
else:
    multiplier= 0.125
# Minimum number of points that need to cross the threshold in a row
min_response_window = 20 
# size of the window to calculate baseline firing (1/2 of it)
baseline_window_size = 20 

# %% CALCULATED SETTINGS
stimulus_duration = np.mean(ns_table.end.values - ns_table.start.values)*1e3
pre_time = round((1/2.)*stimulus_duration,3)
post_time = round((4/3.)*stimulus_duration,3)
window_length = int(pre_time + post_time)
num_trials = stim_table.shape[0]

#%% MAIN CALCULATION
for region in region_list:
    # Time single region
    start_timer = time.time()
    # Identify all units in this structure
    units_in_structure = dataset.unit_df[dataset.unit_df['structure']==region]
    print('Analyzing {} units in {}'.format(len(units_in_structure), str(region)))
    # Identify all probes that probed this structure
    probes_in_structure = units_in_structure['probe'].unique()
    # Initialize list that will contain all the latency info for all units.
    latency = []
    # Initialize the data frame
    col = ['structure', 'probe', 'unit_id', 'depth', 'latency']
    Big_dataframe = pd.DataFrame(columns=col)

    for probe in probes_in_structure: 
        # Get a dictionary of the depths
        depths = {}
        for i, row in units_in_structure[units_in_structure['probe'] == probe].iterrows():
            depths[row['unit_id']] = row['depth']
        # Find the spike times of all the units recorded from this probe
        probe_spikes = dataset.spike_times[probe]
        units_on_probe_in_structure = units_in_structure['unit_id'][units_in_structure['probe']==probe]
        print('    {} contains {} units'.format(probe, len(units_on_probe_in_structure)))
        
        for unit in units_on_probe_in_structure: # Loop through units on probe
            
            raster_matrix = np.zeros((num_trials, window_length))            
            unit_spikes = probe_spikes[unit]
            
            #Loop through every presentation of any image to create raster matrix
            for i,start in enumerate(stim_table.start):
                #Find spikes times between start and end of this trial.
                spike_timestamps = unit_spikes[(unit_spikes > start - pre_time*1e-3) & (unit_spikes <= start + post_time*1e-3)]
                #Subtract start time of stimulus presentation
                spike_timestamps = (spike_timestamps - (start-pre_time*1e-3))*1000
                spike_timestamps = spike_timestamps.astype(int)
                #Add list of spikes to main list
                raster_matrix[i,spike_timestamps] = 1
            
            # Compute SDF on raster matrix    
            sdf = SDF(raster_matrix,5)    
            mean_SDF = sdf.mean(axis=0)
            std_SDF = sdf.std(axis=0)
            SEM_SDF = std_SDF/np.sqrt(num_trials)
            CI95_SDF = SEM_SDF*1.96
            CI99_SDF = SEM_SDF*2.58
    
            #Calculate baseline responses
            #Looking at the 20 msec before and after stim onset
            baseline_mean = np.mean(mean_SDF[pre_time-baseline_window_size:pre_time+baseline_window_size]) 
            baseline_std = np.mean(std_SDF[pre_time-baseline_window_size:pre_time+baseline_window_size])
            baseline_SEM = np.mean(SEM_SDF[pre_time-baseline_window_size:pre_time+baseline_window_size])
            baseline_CI95 = np.mean(CI95_SDF[pre_time-baseline_window_size:pre_time+baseline_window_size]) 
            baseline_CI99 = np.mean(CI99_SDF[pre_time-baseline_window_size:pre_time+baseline_window_size])
    
            post_stimulus_sdf = mean_SDF[pre_time:pre_time+int(stimulus_duration)] #the rest of the sdf after stim onset
            
            #Defines upper threshold as a multiplier of std    
            positive_threshold = baseline_mean + multiplier * std_SDF 
            negative_threshold = baseline_mean - multiplier * std_SDF
        
            #Identify indices that pass the positive threshold
            pos_thresh_inds = post_stimulus_sdf > positive_threshold 
            #Identify indices that pass the negative threshold
            neg_thresh_inds = post_stimulus_sdf < negative_threshold 
            flagged_post_stim_sdf = np.zeros(post_stimulus_sdf.shape) #Initialize an array of zeros 
            flagged_post_stim_sdf[pos_thresh_inds] = 1 #Put a 1 where this threshold is passed
            flagged_post_stim_sdf[neg_thresh_inds] = -1 #Put a 1 where this negative threshold is passed
        
            first_occur = -1 #initialize vector. This value will change if a response is detected
            response_type = np.nan
            for c_ind in range(len(flagged_post_stim_sdf)): #for every indices of this matrix of threshold crossings
                if flagged_post_stim_sdf[c_ind] == 1:
                    if flagged_post_stim_sdf[c_ind:c_ind + min_response_window].sum() == min_response_window: #If the next X time bins all have 1s, the sum should be equal to this windows value
                        first_occur = c_ind #this is the first index after stim onset that meets the requirements
                        response_type = 1 #qualify response as positive
                        break #stop the for loop
                elif flagged_post_stim_sdf[c_ind] == -1: #if the response is negative
                    if flagged_post_stim_sdf[c_ind:c_ind + min_response_window].sum() == -1*min_response_window:
                        first_occur = c_ind
                        response_type = -1
                        break
                    
            # visual response time is empty by default
            response_time = np.nan 
            
            # Define response time as the first occurence, plus the baseline time window
            if first_occur > -1: #if a response was found
                response_time = first_occur + pre_time
            # If the error is null, it is because of a non-firing unit. Discard those
            if positive_threshold < 1: 
                response_time = np.nan
            latency = response_time - pre_time
                  
            Big_dataframe = Big_dataframe.append(pd.DataFrame([[region, probe, unit, depths[unit], latency]], columns=col), ignore_index=True)
    
    print('Region analysis completed in ' + str(round(time.time()-start_timer)) + 'seconds')
    
    #% SAVE EACH REGION
    # Save as .pkl
    fname = os.path.join(save_path, os.path.normpath(region.decode('UTF-8') + '_' + stim_name + '_latency'))
    print('Saving as : {}'.format(fname + '.pkl'))
    f = open(fname + '.pkl', 'wb')
    pickle.dump(Big_dataframe, f)
    f.close()
    
    # Save as .json (for comparison)
    Big_dataframe.to_json(fname + '.json', orient='split')
    
    # % PLOT EACH REGION
    #Plot histogram of latencies for this region
    # Transforms datatype to allow removing the nan entries
    vals = Big_dataframe['latency'].values.astype(float) 
    vals_nonan = vals[~np.isnan(vals)] #remove the nans
    counts, edges = np.histogram(vals_nonan, bins=20)
    centers = edges[:1] - (edges[1]-edges[0])/2
    mean_latency = np.mean(vals_nonan) #calculate the mean latency
    median_latency = np.median(vals_nonan) #calculate the median latency

    try:
        fig,ax1 = plt.subplots(1,1,figsize=(8,5)) #initialize subplot
        plt.hist(vals_nonan, 20) #plot the histogram
        ax1.set_xlabel('Latency of visual response (msec)')
        ax1.set_ylabel('Number of units')
        ax1.set_title(nice_stim_name + ' in ' + str(region))
        y_axis_max = plt_axes.Axes.get_ylim(ax1)[1] 
        ax1.vlines(mean_latency, 0, y_axis_max)
        ax1.vlines(median_latency, 0, y_axis_max)
        plt.text(mean_latency+10, y_axis_max, 'mean = ' + str(round(mean_latency)), fontsize=18)
        plt.text(ax1.get_xlim()[0]+15, y_axis_max, 'median = ' + str(round(median_latency)), fontsize=18)
        plt.grid(True)    
        fig.savefig(fname + '.png')
    except:
        print('Plot for {} failed'.format(region))
            
print('Latency analysis completed in ' + str(round(time.time()-start_timer)) + 'seconds')