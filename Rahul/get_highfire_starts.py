def get_highfire_starts(sdf):
    sdf_trend=sdf;
    sdf_max_idx=np.argmax(sdf_trend);
    sdf_trend_subset=sdf_trend[:sdf_max_idx];
    thresh = -10000;
    minima_idx=argrelextrema(sdf_trend_subset, np.less)[0];
    if not minima_idx:
        return 0;
    else:
        i=1;
        out_idx=minima_idx[len(minima_idx)-i];
        while sdf_trend_subset[out_idx]>thresh:
            out_idx_old=out_idx;
            sdf_sub_2 = sdf[:out_idx];
            thresh=np.percentile(sdf_sub_2,75)
            sdf_trend_subset = sdf_sub_2;
            i+=1;
            out_idx=minima_idx[len(minima_idx)-i];
        idx_temp=argrelextrema(sdf_trend[out_idx:], np.greater)[0][0]
        out_idx=out_idx+(idx_temp/2);
    return out_idx