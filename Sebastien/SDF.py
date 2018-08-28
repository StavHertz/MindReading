def SDF(array, sigma):
    """
    This function accepts a trial by time array of 0s and 1s and returns the spike density function of each trial. 
    It performs a gaussian convolution on each row of the array. Time bins should have milisecond resolution.
    The sigma input specifies the sigma of the gaussian used for convultion (in miliseconds).
    The convolution will produce edge effects. Select a larger than needed time window and cut manually.
    
    @author: SeB
    """
    
    #from __future__ import division #makes sure all divisions are not rounded to nearest integers
    import numpy as np
    import time
    import scipy.stats, scipy.signal
    import scipy as sp
    
    start = time.time() # tic Measures function running speed. Works only on Macs
    
    trials = array.shape[0]
    bins = array.shape[1]
    
    # Create fake data for testing purposes
#    array = np.random.randint(0,2,(trials,bins))
#    sigma = 45
    
    #Define kernel
    sigma = sigma/1000. #Define width of kernel (in sec)
    edges = np.arange(-3*sigma,3*sigma+.001,.001)
    kernel = sp.stats.norm.pdf(edges,0, sigma) #Use a gaussian function
    kernel = kernel*.001 #Time 1/1000 so the total area under the gaussian is 1
    
    #Compute Spike Density Function for all trials
    Sdf = np.zeros((trials,bins))
    Sdf = sp.signal.convolve(array, kernel[None, :] * 1000, mode='same') 
       
    print 'Run time for SDF function was ' + str(round(time.time()-start)) + 'seconds' # toc
     
    return Sdf

    """ End of function """

#%%   
def plot_SDF_per_region(struct, stim, dataset, N):
    """
    This function accepts a structure name (eg. 'TH'), a stimulus type (eg. 'natural_scenes'), your dataset,
    and a number of neurons you want to diplay the SDF and raster plot. It will find across all probes recording
    from structure struct and find all the units.
    
    @author: SeB
    """
    
    # Loop over **ALL** units in a given structure to produce a composite SDF and raster plot over all images
    #Initialize matrix full of zeros
    # Time before and after image presention
    from SDF import SDF
    import matplotlib.pyplot as plt
    import numpy as np
    
    ns_table = dataset.get_stimulus_table(stim) # Load stimulus info for correct category
    
    #Select your structure of interest
    structure_list = dataset.unit_df['structure'].unique() #Identify all brain regions sampled in this experiment
    #################
    #struct = structure_list[6] # Select your structure to analyze here
    #################
    units_in_structure = dataset.unit_df[dataset.unit_df['structure']==struct] #Identify all units in this structure
    probes_in_structure = units_in_structure['probe'].unique() #Identify all probes that probed this structure
    #plt.close("all")
    
    for probe in probes_in_structure: #for each probe recording from this structure
    
        # Find the spike times of all the units recorded from this probe
        probe_spikes = dataset.spike_times[probe]
        unit_on_probe_in_structure = units_in_structure['unit_id'][units_in_structure['probe']==probe]
        
        for unit in unit_on_probe_in_structure[:N]: #for all units recorded from this probe in this area
            
            pre_time = 0.1
            post_time = 0.3
            window_length = int(pre_time*1000 + post_time*1000)
            num_trials = ns_table.shape[0]
            raster_matrix = np.zeros((num_trials, window_length))
            
            unit_spikes = probe_spikes[unit]
            
            #Loop through every presentation of any image
            for i,start in enumerate(ns_table.start):
                #Find spikes times between start and end of this trial.
                spike_timestamps = unit_spikes[(unit_spikes > start - pre_time) & (unit_spikes <= start + post_time)]
                #Subtract start time of stimulus presentation
                spike_timestamps = (spike_timestamps - (start-pre_time))*1000
                spike_timestamps = spike_timestamps.astype(int)
                #Add list of spikes to main list
                raster_matrix[i,spike_timestamps] = 1
            
            #Plotting raster  
            stimulus_duration = ns_table.end.values[0] - ns_table.start.values[0]
            (i,j) = raster_matrix.nonzero()
            fig,ax1 = plt.subplots(1,1,figsize=(6,4))
            color = 'tab:blue'
            ax1.set_ylabel('trials of natural scenes', color=color)
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.axvspan(pre_time*1000,pre_time*1000+stimulus_duration*1000,color='gray',alpha=0.4);
            fig = plt.scatter(j,i,s=0.5)
            plt.xlim(0,window_length)
            ax1.set_xlabel('time (msec)')
            ax1.set_title('Response of unit ' + str(unit) + ' on ' + str(probe) + ' in ' + str(struct) + ' to natural scences')
        
            # Compute SDF on raster matrix    
            sdf = SDF(raster_matrix,5)    
            mean_SDF = sdf.mean(axis=0)
            std_SDF = sdf.std(axis=0)
            SEM_SDF = std_SDF/np.sqrt(num_trials)
            CI95_SDF = SEM_SDF*1.96
            CI99_SDF = SEM_SDF*2.58
            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.set_ylabel('firing rate (Hz)', color=color)
            ax2 = plt.plot(mean_SDF, 'r',linewidth=2)
            ax2 = plt.plot(mean_SDF+CI95_SDF, 'r',linewidth=1,linestyle='dashed')
            ax2 = plt.plot(mean_SDF-CI95_SDF, 'r',linewidth=1,linestyle='dashed')

    """ End of function """