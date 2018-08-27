def get_highfire_starts(sdf,pre_stim_time,min_start_time):
    '''
    This function accepts an array with spike density function values over each milisecond,
    and the time (in seconds) until stimulus onset.
    It estimates and returns the first time (in miliseconds) the neuron started high-firing.
    '''
#    from scipy import signal
    from scipy.stats import iqr
    sdf_stim=sdf[(int(1000*(pre_stim_time))+5):]
    sdf_max_idx=np.argmax(sdf_stim)
    sdf_max_idx_all=argrelextrema(sdf_stim,np.greater)[0]
    if len(sdf_max_idx_all)==0:
        return min_start_time;
    
    thresh0=np.percentile(sdf_stim[sdf_max_idx_all],75)+1.5*iqr(sdf_stim[sdf_max_idx_all]);
    if np.all(df_stim[sdf_max_idx]<thresh0):
        return min_start_time;
    
    sdf_max_idx=np.min(sdf_max_idx_all[sdf_stim[sdf_max_idx_all]>=thresh0])
    
    sdf_stim_subset=sdf_stim[:sdf_max_idx];out_idx=0;
    while True:
        if len(sdf_stim_subset)<3:
            break;
        else:
            out_idx=find_min_highfire(sdf_stim_subset);
#         i=1;
#         while sdf_stim_subset[out_idx]>thresh:
#             relmaxima_temp=argrelextrema(sdf_stim[:out_idx_old], np.greater)[0];
#             if len(relmaxima_temp)>0:
#                 idx_temp0=relmaxima_temp[-1]
#                 if idx_temp0==0:
#                     out_idx=0;
#                     break;
#                 else:
            sdf_stim_subset2 = sdf_stim[:out_idx];
            thresh=np.percentile(sdf_stim_subset2,75)
            if sdf_stim_subset[out_idx]<thresh:
                break;
            else:
                sdf_max_idx2_all=argrelextrema(sdf_stim_subset2,np.greater)[0]
                if len(sdf_max_idx2_all)==0:
                    break;
                sdf_max_idx2=sdf_max_idx2_all[-1]
                sdf_stim_subset2=sdf_stim_subset[:sdf_max_idx2]
                sdf_stim_subset=sdf_stim_subset2;
            
    idx_temp=argrelextrema(sdf_stim[out_idx:], np.greater)[0][0]
    out_idx=out_idx+(idx_temp/2);
    out_idx=out_idx+min_start_time;
    return out_idx