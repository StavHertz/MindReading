def get_highfire_starts(sdf,pre_stim_time,min_start_time):
    '''
    This function estimates and returns the first time (in miliseconds) the neuron starts high-firing.
    Input : An array with spike density function values over each milisecond,
            Time (in seconds) until stimulus onset,
            Minimum latency (in seconds) after stimulus onset
    Output : Index in sdf array where high-firing after stimulus starts
    '''
    from scipy.signal import argrelextrema
    from scipy.stats import iqr
    sdf_stim=sdf[(int(1000*(pre_stim_time))+min_start_time):]
    sdf_max_idx=np.argmax(sdf_stim)
    baseline = sdf[(int(1000*(pre_stim_time))-20):(int(1000*(pre_stim_time))+20)]
    thresh0=np.mean(baseline) + 2* np.std(baseline)
    sdf_max_idx_all=argrelextrema(sdf_stim, np.greater_equal,order=2)[0]
    if len(sdf_max_idx_all)==0:
        return min_start_time;
    
    if np.all(sdf_stim[sdf_max_idx_all]<thresh0):
        return min_start_time;
    
    sdf_max_idx=np.min(sdf_max_idx_all[sdf_stim[sdf_max_idx_all]>=thresh0])
    
    sdf_stim_subset=sdf_stim[:sdf_max_idx];out_idx=0;
    while True:
        if len(sdf_stim_subset)<3:
            break;
        else:
            out_idx=find_min_highfire(sdf_stim_subset);
            sdf_stim_subset2 = sdf_stim[:out_idx];
            thresh=np.percentile(sdf_stim_subset2,75)
            if sdf_stim_subset[out_idx]<thresh:
                break;
            else:
                sdf_max_idx2_all=argrelextrema(sdf_stim_subset2, np.greater_equal,order=2)[0]
                if len(sdf_max_idx2_all)==0:
                    break;
                sdf_max_idx2=sdf_max_idx2_all[-1]
                sdf_stim_subset2=sdf_stim_subset[:sdf_max_idx2]
                sdf_stim_subset=sdf_stim_subset2;
            
    idx_temp=argrelextrema(sdf_stim[out_idx:],np.greater_equal,order=2)[0][0]
    out_idx=out_idx+(idx_temp/2);
    out_idx=out_idx+min_start_time;
    return out_idx