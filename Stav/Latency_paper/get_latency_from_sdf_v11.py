import numpy as np
from get_prestimulus_time import get_prestimulus_time
from get_time_window_buffer import get_time_window_buffer
from get_baseline_window_size import get_baseline_window_size

def get_latency_from_sdf_v11(sdf, number_of_std=4, min_response_window=10):
    baseline_window_size = get_baseline_window_size()
    pre_stimulus_time = get_prestimulus_time() - get_time_window_buffer()
    baseline_stimulus_sdf = sdf[pre_stimulus_time-baseline_window_size:pre_stimulus_time+baseline_window_size]
    post_stimulus_sdf = sdf[pre_stimulus_time:]

    pre_std_val = np.std(baseline_stimulus_sdf)
    pre_mean_val = np.mean(baseline_stimulus_sdf)
    positive_threshold = pre_mean_val + number_of_std*pre_std_val
    negative_threshold = pre_mean_val + -1*number_of_std*pre_std_val

    pos_thresh_inds = post_stimulus_sdf > positive_threshold
    neg_thresh_inds = post_stimulus_sdf < negative_threshold
    flagged_post_stim_sdf = np.zeros(post_stimulus_sdf.shape)
    flagged_post_stim_sdf[pos_thresh_inds] = 1
    flagged_post_stim_sdf[neg_thresh_inds] = -1

    first_occur = -1
    response_type = np.nan
    for c_ind in range(len(flagged_post_stim_sdf)):
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