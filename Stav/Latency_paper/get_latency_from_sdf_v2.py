from scipy.stats import iqr
from scipy.signal import argrelextrema
from get_prestimulus_time import get_prestimulus_time
from get_time_window_buffer import get_time_window_buffer
import numpy as np

def find_min_highfire(a):
    idx_range = np.arange(len(a))
    for idx in idx_range[::-1][1:-1]:
        if (a[idx]<a[idx+1]) and (a[idx]<=a[idx-1]):
            break;
    if idx==2:
        idx=1
    return(idx)

def get_latency_from_sdf_v2(mean_sdf):
    pre_stimulus_time = get_prestimulus_time() - get_time_window_buffer()

    used_percentile = 75
    sdf_stim=mean_sdf[pre_stimulus_time:]
    sdf_max_idx=np.argmax(sdf_stim)
    sdf_max_idx_all=argrelextrema(sdf_stim,np.greater)[0]
    
    if len(sdf_max_idx_all)==0:
        return np.nan, np.nan
    
    thresh0=np.percentile(sdf_stim[sdf_max_idx_all], used_percentile) +  \
    1.5*iqr(sdf_stim[sdf_max_idx_all])

    if np.all(sdf_stim[sdf_max_idx]<thresh0):
        return np.nan, np.nan
    
    sdf_max_idx=np.min(sdf_max_idx_all[sdf_stim[sdf_max_idx_all]>=thresh0])
    
    sdf_stim_subset=sdf_stim[:sdf_max_idx]
    out_idx=0
    
    continue_looping = True
    while continue_looping:
        if len(sdf_stim_subset)<3:
            continue_looping = False
        else:
            out_idx=find_min_highfire(sdf_stim_subset);
            sdf_stim_subset2 = sdf_stim[:out_idx];
            thresh=np.percentile(sdf_stim_subset2,75)
            if sdf_stim_subset[out_idx]<thresh:
                continue_looping = False
            else:
                sdf_max_idx2_all=argrelextrema(sdf_stim_subset2,np.greater)[0]
                if len(sdf_max_idx2_all)==0:
                    continue_looping = False
                else:
	                sdf_max_idx2=sdf_max_idx2_all[-1]
	                sdf_stim_subset2=sdf_stim_subset[:sdf_max_idx2]
	                sdf_stim_subset=sdf_stim_subset2
            
    idx_temp=argrelextrema(sdf_stim[out_idx:], np.greater)[0][0]
    out_idx=out_idx+(idx_temp/2)
    out_idx=out_idx
    response_type = 1
    return out_idx, response_type
