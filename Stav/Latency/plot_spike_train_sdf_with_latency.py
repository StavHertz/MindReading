# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:41:41 2018

@author: Stav
"""

import numpy as np
import matplotlib.pyplot as plt
from get_hist_sdf import get_hist_sdf
from print_info import print_info

def time_in_ms_to_index(ms_time):
    return ms_time + 100

def index_to_time_in_ms(arr_ind):
    return float(arr_ind)/float(1000)

def plot_spike_train_sdf_with_latency(spike_train, fig_path):
    number_of_std = 3
    window_in_ms = float(10) # 5
    first_possible_response = 50
    start_window_in_ms = float(-100)
    end_window_in_ms = float(250)
    window_in_secs = window_in_ms/float(1000)
    min_range = int(float(-100)/window_in_ms)
    max_range = int(float(250)/window_in_ms + 1)

    x_axis_values = [float(x)/float(1000) for x in range(min_range*int(window_in_ms), (max_range-1)*int(window_in_ms))]

    fig,ax = plt.subplots(1,1,figsize=(6,3))

    sdfs = np.zeros((len(spike_train), int(end_window_in_ms-start_window_in_ms)))
    for row_ind, row in enumerate(spike_train):
        sdf = get_hist_sdf(row)
        sdfs[row_ind, :] = sdf
    mean_sdf = sdfs.mean(axis=0)

    max_sdf_val = mean_sdf.max()
    ax.set_ylim([0, max_sdf_val])
    num_of_trains = len(spike_train)
    y_spike_locations = [(max_sdf_val/float(num_of_trains))*x for x in range(num_of_trains)]

    for r_ind, row in enumerate(spike_train):
        ax.plot(row, y_spike_locations[r_ind]*np.ones_like(row),'|',color='b')

    plt.plot(x_axis_values, mean_sdf, color='black')

    zero_ind = time_in_ms_to_index(0)
    pre_stimulus_vals = mean_sdf[:zero_ind]
    post_stimulus_val = mean_sdf[zero_ind:]

    pre_std_val = np.std(pre_stimulus_vals)
    pre_mean_val = np.mean(pre_stimulus_vals)
    positive_threshold = pre_mean_val + number_of_std*pre_std_val
    negative_threshold = pre_mean_val + -1*number_of_std*pre_std_val
    post_stimulus_arr = np.array(post_stimulus_val)

    first_occur = -1
    pos_first_occur = -1
    neg_first_occur = -1

    if post_stimulus_arr.max() > positive_threshold:
        pos_first_occur = np.argmax(post_stimulus_arr > positive_threshold)

    if post_stimulus_arr.min() < negative_threshold:
        neg_first_occur = np.argmax(post_stimulus_arr < negative_threshold)

    if pos_first_occur > -1 and neg_first_occur > -1:
        if pos_first_occur < neg_first_occur:
            first_occur = pos_first_occur
            plt.axvline(x=index_to_time_in_ms(first_occur), color='green',alpha=0.5)    		
        else:
            first_occur = neg_first_occur
            plt.axvline(x=index_to_time_in_ms(first_occur), color='red',alpha=0.5)    		
    else:
        if pos_first_occur > -1:
            first_occur = pos_first_occur
            plt.axvline(x=index_to_time_in_ms(first_occur), color='green',alpha=0.5)    		    		
        elif neg_first_occur > -1:
            first_occur = neg_first_occur
            plt.axvline(x=index_to_time_in_ms(first_occur), color='red',alpha=0.5)

    ax.axvspan(start_window_in_ms/float(1000),0,color='gray',alpha=0.2)
    ax.set_xlim([start_window_in_ms/float(1000), end_window_in_ms/float(1000)])

    fig.savefig(fig_path)

    response_time = float('nan')
    if first_occur > -1:
        response_time = zero_ind+first_occur

    return response_time