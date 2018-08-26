def get_highfire_starts(sdf,pre_stim_time):
    '''
    This function accepts an array with spike density function values over each milisecond,
    and the time (in seconds) until stimulus onset.
    It estimates and returns the first time (in miliseconds) the neuron started high-firing.
    '''
    sdf_stim=sdf[int(1000*pre_stim_time):]
    sdf_max_idx=np.argmax(sdf_stim)
    sdf_stim_subset=sdf_stim[:sdf_max_idx];
    thresh = -10000;
    minima_idx=argrelextrema(sdf_stim_subset, np.less)[0];
    if not minima_idx:
        out_idx=0;
        final_chunk = sdf_stim[out_idx:]
        out_idx=out_idx+np.where(final_chunk>final_chunk[0])[0][0]-1
    else:
        i=1;
        out_idx=minima_idx[len(minima_idx)-i];
        while sdf_stim_subset[out_idx]>thresh:
            out_idx_old=out_idx;
            sdf_sub_2 = sdf[:out_idx];
            thresh=np.percentile(sdf_sub_2,75)
            sdf_stim_subset = sdf_sub_2;
            i+=1;
            out_idx=minima_idx[len(minima_idx)-i];
    idx_temp=argrelextrema(sdf_stim[out_idx:], np.greater)[0][0]
    out_idx=out_idx+(idx_temp/2);
    return out_idx