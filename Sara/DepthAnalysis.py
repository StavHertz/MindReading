# -*- coding: utf-8 -*-
"""
Analysis of latency as a function of depth

Created on Tue Aug 28 21:45:02 2018

@author: sarap
"""
import os
import sys
import pickle
import numpy as np
import scipy.signal
import matplotlib.pylab as plt
import seaborn as sns
sns.set_context('talk', font_scale=2, rc={'lines.markeredgewidth': 2})
sns.plotting_context(rc={'font.size': 18})
sns.set_style('white')
sns.set_palette('deep');

#%% IMPORTS FROM MINDREADING REPOSITORY
sys.path.append('D:/resources/mindreading/Sara/')
from neuropixel_data import open_experiment, check_folder
from neuropixel_plots import region_color

sys.path.append('D:/resources/mindreading/Sebastien/')
from SDF import SDF

#%% IMPORT DATA IF NEEDED
drive_path = os.path.normpath('d:/visual_coding_neuropixels/')
dataset = open_experiment(drive_path, 3)
#%% REGISTER PATH
expt_index = dataset.nwb_path[-6:-4]
print('Current experiment index: {}'.format(expt_index))
#%% INFORMATION FOR SAVING
depth_path = os.path.normpath('D:/Depths/{}/'.format(expt_index))
latency_path = os.path.normpath('D:/Latencies/{}/'.format(expt_index))
print('Importing from : ', latency_path)
print('Saving to: ', depth_path)
check_folder(depth_path)

stim_name = 'drifting_gratings'
nice_stim_name = 'Drifting Gratings'
#%% ANALYSIS PARAMETERS
sg_bins = 20
sg_window = 5
sg_order = 2
hist_bins = 10

# Plot mean and median with SEM
do_errplot = True
#%% Cycle through areas
regions = {'VISpm', 'VISam', 'VISp', 'VISl', 'VISal', 'VISrl', 'TH', 'SCs', 'DG', 'CA'}
#col = ['depth', 'latency', 'unit_id', 'depth', 'latency']
 #   Big_dataframe = pd.DataFrame(columns=col)
main_fig, main_ax = plt.subplots()
#depth_latency_df
for region in regions:
    fpath = os.path.join(latency_path, '{}_{}_latency'.format(region, stim_name))
    spath = os.path.join(depth_path, '{}_{}_depth'.format(region, stim_name))
    if not os.path.exists(fpath + '.pkl'):
        print('No .pkl file found for {}'.format(region))
        continue
    f = open(fpath+'.pkl')
    depth_df = pickle.load(f)
    f.close()
    not_nan = depth_df['latency'].notna()
    if len(np.where(not_nan.values == True)[0]) <= sg_window:
        print('Region {} has only {} non-nan data points'.format(region, len(np.where(not_nan.values==True)[0])))
        continue

    # Clip out the NaNs
    depths = depth_df['depth'].values
    latencies = depth_df['latency'].values
    depths = depths[depth_df['latency'].notna()]
    latencies = latencies[depth_df['latency'].notna()]
    
    # Remove latencies beyond 250 ms (only important for drifting grating)
    ind = np.where(latencies < 250)
    if len(ind) is not len(latencies):
        print('{} of {} latencies over 250 ms'.format(len(latencies)-len(ind[0]), len(latencies)))
    depths = depths[ind]
    latencies = latencies[ind]

    if do_errplot:
        counts, edges = np.histogram(depths, bins=np.arange(np.min(depths), np.max(depths), 50))
        latency_mean = np.zeros_like(counts)
        latency_median = np.zeros_like(counts)
        latency_std = np.zeros_like(counts)    
        for i in range(len(edges)-1):
            ind = np.where((depths >= edges[i]) & (depths < edges[i+1]))
            latency_mean[i] = np.mean(latencies[ind])
            latency_median[i] = np.median(latencies[ind])
            latency_std[i] = np.std(latencies[ind])
        latency_sem = latency_std/np.sqrt(len(latency_std))
        
        # Remove the last edge
        bin_centers = edges[:-1]-((edges[1]-edges[0])/2)   
        
        # Remove the edges without any values
        ind = np.where(latency_mean > 2)
    
        fig, ax = plt.subplots()
        ax.plot(depths, latencies, marker='o', linestyle='none', color='k', alpha=0.2)
        ax.errorbar(bin_centers[ind], latency_mean[ind], yerr=latency_sem[ind], marker='o', label='mean')
        ax.plot(bin_centers[ind], latency_median[ind], marker='o', label='median')
        ax.set_ylabel('Latency (ms)')
        ax.set_xlabel('Depth (um)')
        ax.set_title('{} - {} ({})'.format(region, nice_stim_name, expt_index))
        ax.set_ylim(0,)
        fig.savefig(spath + '_scatter.png')

    
    g = sns.jointplot(latencies, depths, kind="kde", height=7, space=0, stat_func=None, color=region_color(region))
    g.plot_marginals(sns.rugplot, height=0.1, color="k")
    g.set_axis_labels(xlabel='{} latency (ms)'.format(region), ylabel='{} depth (mm) '.format(region))
    g.savefig(spath + '.png')
    
    # Do it again for smooth curve
    if len(np.where(not_nan.values == True)[0]) < sg_window:
        print('Skipping smooth curve plot for {}'.format(region))
        continue
    # Upsampled histogram
    counts, edges = np.histogram(depth_df['depth'], bins=sg_bins)
    # Get the mean latency for each bin
    latency_mean = np.zeros_like(counts)
    latency_median = np.zeros_like(counts)
    for i in range(len(edges)-1):
        ind = np.where((depths >= edges[i]) & (depths < edges[i+1]))
        latency_mean[i] = np.median(latencies[ind])
        latency_median[i] = np.mean(latencies[ind])
    bin_centers = edges[:-1] - (edges[1]-edges[0])/2
    # Get indices of empty bins
    ind = np.where(latency_mean > 2)
    if len(ind[0]) < sg_window:
        print('Skipping smooth curve plot for {}'.format(region))
        continue
    print('{}-{} bin size = {} ms'.format(expt_index, region, (np.max(edges)-np.min(edges))/sg_bins))
    
    # Smooth curve plot    
    fig, ax = plt.subplots()
    ax.plot(bin_centers[ind], scipy.signal.savgol_filter(latency_mean[ind], sg_window, sg_order), linewidth=3)
    #ax.plot(bin_centers[ind], scipy.signal.savgol_filter(latency_median[ind], sg_window, sg_order), linewidth=3)
    ax.plot(depths, latencies, marker='o', linestyle='none', alpha=0.2, color='k')
    ax.set_ylim(0,)
    ax.set_title('{} - {} ({})'.format(region, nice_stim_name, expt_index))
    ax.set_xlabel('Depth (um)')
    ax.set_ylabel('Latency (ms)')
    fig.savefig(spath + '_smooth.png')
    
    main_ax.plot((bin_centers[ind]-np.max(bin_centers[ind]))/np.max(np.abs(bin_centers[ind])), scipy.signal.savgol_filter(latency_mean[ind], sg_window, sg_order), linewidth=3, label=region)

main_ax.set_xlabel('Depth (um)')
main_ax.set_ylabel('Time (ms)')
main_ax.set_title('{} {}'.format(expt_index, nice_stim_name))
main_ax.legend()
main_fig.savefig(os.path.join(save_path, '{}_{}.png'.format(expt_index, stim_name)))
