"""
Build distribution of latencies for entire experiment

Created on Tue Aug 28 22:24:19 2018

@author: SeB
Sara version
"""
print('Loading session information...')
# We need to import these modules to get started
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys
sys.path.append('/Users/SeB/Desktop/Allen Brain Workshop/SWDB_2018/resources/swdb_2018_neuropixels/')
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter
import pickle
from SDF import SDF
import matplotlib.axes as plt_axes
import time

start_timer = time.time() # tic Measures function running speed. Works only on Macs
# set path for manifest file 
drive_path = '/Users/SeB/Desktop/Allen Brain Workshop/SWDB_2018/resources/visual_coding_neuropixels'

# identify manifest file
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')

# Create a dataframe 
expt_info_df = pd.read_csv(manifest_file)

#make new dataframe by selecting only multi-probe experiments
multi_probe_expt_info = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

#%%
for experiment_counter in [2]: # for each multiprobe experiment

    multi_probe_filename  = multi_probe_expt_info.iloc[experiment_counter]['nwb_filename']
    print('*****************************************')
    print('Analyzing session ' + multi_probe_filename)
    print('*****************************************')
    
    # Specify full path to the .nwb file
    nwb_file = os.path.join(drive_path,multi_probe_filename)
    
    #Load dataset for this specific experiment
    dataset = NWB_adapter(nwb_file)
    
    # initialize dictionary for all stimuli type
    Session_dict = {}
    
    #Select your structure of interest
    structure_list = dataset.unit_df['structure'].unique() #Identify all brain regions sampled in this experiment
    
    valid_stim = ['drifting_gratings'] 
    # Only these stimuli types have a clear onset and a wide-field stimulation.

    for stimulus_type in valid_stim: #Major loop across stimulus type for this recording session
        
        if stimulus_type == 'drifting_gratings':
            multiplier = 0.25 #Drifting gratings require a more stringent multipliers because of more noisy SDF function over long time windows
        else:
            multiplier = 0.125
            
        ns_table = dataset.get_stimulus_table(stimulus_type)
        stimulus_duration = np.mean(ns_table.end.values - ns_table.start.values)
        
        col = ['region', 'probe', 'unit_id', 'depth','latency']
        Big_dataframe = pd.DataFrame(columns=col) #Initialize big dataframe that will contain all info for this stimulus type
        
        for struct in structure_list: # Select your structure to analyze here
            
            units_in_structure = dataset.unit_df[dataset.unit_df['structure']==struct] #Identify all units in this structure
            probes_in_structure = units_in_structure['probe'].unique() #Identify all probes that probed this structure
    
            for probe in probes_in_structure: #for each probe recording from this structure
                probe_df = units_in_structure[units_in_structure['probe'] == probe]
                depths = {}
                for i, row in probe_df.iterrows():
                    depths[row['unit_id']] = row['depth']
                
                # Find the spike times of all the units recorded from this probe
                probe_spikes = dataset.spike_times[probe]
                unit_on_probe_in_structure = units_in_structure['unit_id'][units_in_structure['probe']==probe]
                
                for unit in unit_on_probe_in_structure: #for all units recorded from this probe in this area
                    
                    pre_time = round((1/2.)*stimulus_duration,3) #fix the time window as a proportion of stim duration to account or different stim durations across stim types.
                    post_time = round((4/3.)*stimulus_duration,3)
                    window_length = int(pre_time*1000 + post_time*1000)
                    num_trials = ns_table.shape[0]
                    raster_matrix = np.zeros((num_trials, window_length))
                    
                    unit_spikes = probe_spikes[unit]
                    
                    #Loop through every presentation of any image to create raster matrix
                    for i,start in enumerate(ns_table.start):
                        #Find spikes times between start and end of this trial.
                        spike_timestamps = unit_spikes[(unit_spikes > start - pre_time) & (unit_spikes <= start + post_time)]
                        #Subtract start time of stimulus presentation
                        spike_timestamps = (spike_timestamps - (start-pre_time))*1000
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
            
                    #Compute latency
                    min_response_window = 20 #Minimum number of points that need to cross the threshold in a row
                    baseline_window_size = 20 #size of the window to calculate baseline firing (1/2 of it)
                    pre_stimulus_time = int(pre_time*1000) # time stim onset in SDF data
                    
                    #Calculate baseline responses
                    baseline_mean = np.mean(mean_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
                    baseline_std = np.mean(std_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
                    baseline_SEM = np.mean(SEM_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
                    baseline_CI95 = np.mean(CI95_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
                    baseline_CI99 = np.mean(CI99_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
            
                    post_stimulus_sdf = mean_SDF[pre_stimulus_time:(pre_stimulus_time+int(stimulus_duration*1000))] #the rest of the sdf after stim onset
                
                    positive_threshold = baseline_mean + (multiplier * baseline_std) #Defines upper threshold as a multiplier of std
                    negative_threshold = baseline_mean - (multiplier * baseline_std) #Defines upper threshold as a multiplier of std
                     
                    pos_thresh_inds = post_stimulus_sdf > positive_threshold #Identify indices that pass the positive threshold
                    neg_thresh_inds = post_stimulus_sdf < negative_threshold #Identify indices that pass the negative threshold
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
                
                    response_time = np.nan #visual response time is empty by default
                    if first_occur > -1: #if a response was found
                        response_time = first_occur + pre_stimulus_time#define response time as the first occurence, plus the baseline time window
                    if positive_threshold < 1: # If the error is null, it is because of a non-firing unit. Discard those
                        response_time = np.nan
                    
                    latency = response_time - pre_stimulus_time
                          
                    Big_dataframe = Big_dataframe.append(pd.DataFrame([[struct, probe, unit, depths[unit],latency]], columns=col), ignore_index=True)
                    
                print('*****************************************')
                print('Finished ' + probe + ' in area ' + struct + ' for ' + stimulus_type + ' in session ' + multi_probe_filename)
                print('*****************************************')
                
            #Plot histogram of latencies for this region
            vals = Big_dataframe['latency'].values.astype(float)[Big_dataframe['region']==struct] #transforms datatype  to allow removing the nan entries
            vals_nonan = vals[~np.isnan(vals)] #remove the nans
            num_neurons_in_area = len(vals)
            num_responsive = len(vals_nonan)
            mean_latency = np.mean(vals_nonan) #calculate the mean latency
            median_latency = np.median(vals_nonan) #calculate the median latency
            
            fig,ax1 = plt.subplots(1,1,figsize=(6,4)) #initialize subplot
            plt.hist(vals_nonan, 20, [0, 200]) #plot the histogram
            ax1.set_xlabel('Latency of visual response (msec)')
            ax1.set_ylabel('Number of units')
            plt.xlim(0, 200)
            ax1.set_title('Latency to ' + stimulus_type + ' in ' + str(struct) + ' in session ' + multi_probe_filename[12:-4])
            y_axis_max = plt_axes.Axes.get_ylim(ax1)[1] #find the maximum y value of the histogram for later ploting
            ax1.plot([mean_latency, mean_latency], [0,y_axis_max], color='r', linestyle='-', linewidth=2)# plot the mean
            ax1.plot([median_latency, median_latency], [0,y_axis_max], color='m', linestyle='-', linewidth=2) #plot the median
            plt.text(mean_latency+5, y_axis_max, 'mean = ' + str(round(mean_latency))) #add text
            plt.text(median_latency-40, y_axis_max, 'med = ' + str(round(median_latency)))
            plt.text(mean_latency+5, y_axis_max/2, str(num_responsive) + '/' + str(num_neurons_in_area) + ' responsive')
            plt.grid(True) #plot the grid
                
        #Pool Stimulus dataframe on session dictionnary
        Session_dict[stimulus_type] = Big_dataframe
        
    ## Save file for each session
    with open(multi_probe_filename[:-4] + '.pkl', 'w') as f:  
        pickle.dump([Session_dict], f)    
            
print 'Latency analysis completed in ' + str(round(time.time()-start_timer)) + 'seconds' # toc
