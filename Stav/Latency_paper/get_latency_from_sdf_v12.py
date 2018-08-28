import numpy as np
from get_prestimulus_time import get_prestimulus_time
from get_time_window_buffer import get_time_window_buffer
from get_baseline_window_size import get_baseline_window_size

def get_latency_from_sdf_v12(all_sdfs, number_of_std=3, min_response_window=10):
    baseline_window_size = get_baseline_window_size()
    pre_stimulus_time = get_prestimulus_time() - get_time_window_buffer()
    post_stimulus_sdf = mean_SDF[pre_stimulus_time:] #the rest of the sdf after stim onset

    mean_SDF = all_sdfs.mean(axis=0)
    std_SDF = all_sdfs.std(axis=0)
    SEM_SDF = std_SDF/np.sqrt(len(all_sdfs))
    CI95_SDF = SEM_SDF*1.96
    CI99_SDF = SEM_SDF*2.58

    #Compute latency
    multiplier = number_of_std #Multiplier of standard errors for threshold detection

    #Calculate baseline responses
    baseline_mean = np.mean(mean_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
    baseline_std = np.mean(std_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
    baseline_SEM = np.mean(SEM_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
    baseline_CI95 = np.mean(CI95_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset
    baseline_CI99 = np.mean(CI99_SDF[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]) #Looking at the 20 msec before and after stim onset

    positive_threshold = baseline_mean + multiplier * baseline_CI95 #Defines upper threshold as a multiplier of std
    negative_threshold = baseline_mean - multiplier * baseline_CI95 #Defines upper threshold as a multiplier of std

    pos_thresh_inds = post_stimulus_sdf > positive_threshold
    neg_thresh_inds = post_stimulus_sdf < negative_threshold
    flagged_post_stim_sdf = np.zeros(post_stimulus_sdf.shape)
    flagged_post_stim_sdf[pos_thresh_inds] = 1
    flagged_post_stim_sdf[neg_thresh_inds] = -1

    first_occur = -1
    response_type = np.nan
    for c_ind in range(len(flagged_post_stim_sdf) - min_response_window):
        if flagged_post_stim_sdf[c_ind] == 1:
            if flagged_post_stim_sdf[c_ind:c_ind + min_response_window].sum() == min_response_window:
                first_occur = c_ind
                response_type = 1
                break # Sorry
        elif flagged_post_stim_sdf[c_ind] == -1:
            if flagged_post_stim_sdf[c_ind:c_ind + min_response_window].sum() == -1*min_response_window:
                first_occur = c_ind
                response_type = -1
                break

    response_time = np.nan
    if first_occur > -1:
        response_time = first_occur

    pre_stim_dict = {}
    pre_stim_dict['mean'] = pre_mean_val
    pre_stim_dict['std'] = pre_std_val
    pre_stim_dict['std_num'] = number_of_std
    pre_stim_dict['min_response_window'] = min_response_window

    return response_time, response_type, pre_stim_dict